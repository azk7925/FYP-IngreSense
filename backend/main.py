from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import torch
from transformers import AutoTokenizer
import os
import numpy as np

from backend.model import HybridCosmeticClassifier, IngredientKnowledgeGraph
from backend.knowledge_base import INGREDIENT_KNOWLEDGE_BASE
from backend.utils import clean_ingredient_text, extract_ingredients

app = FastAPI(title="IngreSense API", description="Cosmetic Ingredient Classification API")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
model = None
tokenizer = None
kg = None
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = "backend/models/best_model.pt"

# Request model
class IngredientRequest(BaseModel):
    ingredients: str

# Response models
class IngredientExplanation(BaseModel):
    name: str
    status: str  # e.g. "Safe", "Not Vegan", "Unknown"
    details: str

class ClassificationResult(BaseModel):
    label: str
    probability: float
    is_present: bool

class AnalysisResponse(BaseModel):
    results: List[ClassificationResult]
    explanations: List[IngredientExplanation]
    model_status: str  # "Active" or "Mock Mode"

@app.on_event("startup")
async def startup_event():
    global model, tokenizer, kg
    
    print("Initialize Knowledge Graph...")
    kg = IngredientKnowledgeGraph(INGREDIENT_KNOWLEDGE_BASE)
    
    print("Loading Tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    
    print(f"Checking for model at {MODEL_PATH}...")
    if os.path.exists(MODEL_PATH):
        try:
            print("Loading Model...")
            model = HybridCosmeticClassifier(
                transformer_name='bert-base-uncased',
                kg_feature_dim=9,
                num_labels=4
            )
            # Load state dict
            checkpoint = torch.load(MODEL_PATH, map_location=device)
            if 'model_state_dict' in checkpoint:
                model.load_state_dict(checkpoint['model_state_dict'])
            else:
                model.load_state_dict(checkpoint)
            model.to(device)
            model.eval()
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Failed to load model: {e}")
            model = None
    else:
        print("Model file not found. Running in Mock Mode.")
        model = None

@app.get("/health")
def health_check():
    return {"status": "healthy", "mode": "active" if model else "mock"}

@app.post("/classify", response_model=AnalysisResponse)
async def classify_ingredients(request: IngredientRequest):
    text = request.ingredients
    if not text.strip():
        raise HTTPException(status_code=400, detail="No ingredients provided")

    # Preprocess
    cleaned_text = clean_ingredient_text(text)
    ing_list = extract_ingredients(cleaned_text)
    
    # Explanations from KG (Determininstic)
    explanations = []
    
    # Track aggregate scores for simple mock logic if needed
    halal_score = 0
    vegan_score = 0
    allergen_score = 0
    eco_score = 0
    count = 0
    
    for ing in ing_list:
        lookup = kg.lookup(ing)
        props = lookup['properties']
        
        # Determine status string
        status_parts = []
        if props.get('halal') < 0.5: status_parts.append("Not Halal")
        if props.get('vegan') < 0.5: status_parts.append("Not Vegan")
        if props.get('allergen') > 0.5: status_parts.append("Allergen")
        
        status = ", ".join(status_parts) if status_parts else "Safe"
        if not lookup['found']:
            status = "Unknown"
        
        explanations.append(IngredientExplanation(
            name=lookup.get('canonical_name', ing),
            status=status,
            details=props.get('reasoning', "No data available")
        ))
        
        if lookup['found']:
            halal_score += props.get('halal', 0.5)
            vegan_score += props.get('vegan', 0.5)
            allergen_score += props.get('allergen', 0.5)
            eco_score += props.get('eco', 0.5)
            count += 1
    
    if count == 0: count = 1 # Avoid div by zero

    # Classification
    results = []
    label_names = ['Halal', 'Vegan', 'Allergen Free', 'Eco-Friendly'] # Note: Logic inverse for Allergen? 
    # Dataset labels were: halal, vegan, allergen, eco.
    # Usually 'Allergen' label=1 means "Contains allergens". 
    # Let's assume the model outputs: [Halal, Vegan, Has_Allergen, Eco]
    
    if model:
        # Prepare inputs
        kg_features = kg.extract_features(ing_list)
        encoding = tokenizer(
            cleaned_text,
            max_length=256,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        input_ids = encoding['input_ids'].to(device)
        attention_mask = encoding['attention_mask'].to(device)
        kg_tensor = torch.tensor(kg_features, dtype=torch.float32).unsqueeze(0).to(device)
        
        try:
            with torch.no_grad():
                logits = model(input_ids, attention_mask, kg_tensor)
                probs = torch.sigmoid(logits).cpu().numpy()[0]
                
            # Construct results
            # idx 0: Halal
            results.append(ClassificationResult(label="Halal", probability=float(probs[0]), is_present=probs[0]>0.5))
            # idx 1: Vegan
            results.append(ClassificationResult(label="Vegan", probability=float(probs[1]), is_present=probs[1]>0.5))
            # idx 2: Allergen (Logic: is_present=True means "Contains Allergen")
            # But UI might want "Allergen Free". Let's stick to what the model predicts for now: "Contains Allergen"
            results.append(ClassificationResult(label="Contains Allergens", probability=float(probs[2]), is_present=probs[2]>0.5))
            # idx 3: Eco
            results.append(ClassificationResult(label="Eco-Friendly", probability=float(probs[3]), is_present=probs[3]>0.5))
            
        except Exception as e:
            print(f"Inference error: {e}")
            # Fallback to mock if runtime error
            return _get_mock_results(halal_score/count, vegan_score/count, allergen_score/count, eco_score/count, explanations)

    else:
        # Mock Mode
        return _get_mock_results(halal_score/count, vegan_score/count, allergen_score/count, eco_score/count, explanations)

    return AnalysisResponse(
        results=results,
        explanations=explanations,
        model_status="Active" if model else "Mock Mode"
    )

def _get_mock_results(h, v, a, e, explanations):
    # Simple heuristic for mock mode
    return AnalysisResponse(
        results=[
            ClassificationResult(label="Halal", probability=h, is_present=h>0.6),
            ClassificationResult(label="Vegan", probability=v, is_present=v>0.6),
            ClassificationResult(label="Contains Allergens", probability=a, is_present=a>0.4),
            ClassificationResult(label="Eco-Friendly", probability=e, is_present=e>0.6),
        ],
        explanations=explanations,
        model_status="Mock Mode"
    )

# Explanability Logic rewritten natively here

def explain_with_ontology(text: str):
    '''Get knowledge graph evidence for each ingredient'''
    clean_text = clean_ingredient_text(text)
    ing_list = extract_ingredients(clean_text)

    evidence = []
    ambiguous = []

    for ing in ing_list:
        result = kg.lookup(ing)
        props = result['properties']

        evidence_item = {
            'ingredient': ing,
            'found': result['found'],
            'canonical_name': result.get('canonical_name', ing),
            'source': props.get('source', 'unknown'),
            'scores': {
                'halal': props.get('halal', 0.5),
                'vegan': props.get('vegan', 0.5),
                'allergen': props.get('allergen', 0.5),
                'eco': props.get('eco', 0.5)
            },
            'reasoning': props.get('reasoning', 'No information available')
        }

        evidence.append(evidence_item)

        # Flag ambiguous ingredients
        if not result['found'] or props.get('source') == 'ambiguous':
            ambiguous.append({
                'ingredient': ing,
                'reason': 'Not found in knowledge base' if not result['found'] else 'Ambiguous source'
            })

    return evidence, ambiguous

@app.post("/explain")
async def get_detailed_explanation(request: IngredientRequest):
    text = request.ingredients
    if not text.strip():
        raise HTTPException(status_code=400, detail="No ingredients provided")
        
    # Get basic predictions by reusing logic (we run the model here again to extract probabilities)
    # We could also accept the probabilities from the frontend, but it's safer to re-evaluate
    clean_text = clean_ingredient_text(text)
    ing_list = extract_ingredients(clean_text)
    
    predictions = {}
    label_names = ['Halal', 'Vegan', 'Allergen-Safe', 'Eco-Friendly'] 
    
    if model:
        kg_features = kg.extract_features(ing_list)
        encoding = tokenizer(
            clean_text,
            max_length=256,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        input_ids = encoding['input_ids'].to(device)
        attention_mask = encoding['attention_mask'].to(device)
        kg_tensor = torch.tensor(kg_features, dtype=torch.float32).unsqueeze(0).to(device)
        
        try:
            with torch.no_grad():
                logits = model(input_ids, attention_mask, kg_tensor)
                probs = torch.sigmoid(logits).cpu().numpy()[0]
                
            # In prediction endpoint: index 2 is "Contains Allergens". Let's convert to Allergen-Safe here to match frontend expectation or keep it raw
            for i, label in enumerate(label_names):
                prob = float(probs[i])
                prediction = 'Positive' if prob > 0.5 else 'Negative'
                
                # Invert logic for Allergen-Safe so > 0.5 means Safe
                if i == 2:
                    prob = 1.0 - prob
                    prediction = 'Positive' if prob > 0.5 else 'Negative'
                
                confidence = abs(prob - 0.5) * 2
                predictions[label] = {
                    'prediction': prediction,
                    'probability': round(prob, 4),
                    'confidence': round(confidence, 4)
                }
        except Exception as e:
            print(f"XAI inference error: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to run model explanation: {e}")
            
    else:
        raise HTTPException(status_code=503, detail="Model is currently unavailable for detailed explanation. Running in mock mode.")

    # Get ontology evidence
    evidence, ambiguous = explain_with_ontology(text)

    # Format for API
    api_response = {
        'predictions': predictions,
        'top_contributors': {},
        'kg_evidence': [],
        'ambiguous_ingredients': ambiguous,
        'confidence_level': 'medium'
    }

    # Top contributors per label
    label_mapping = {'Halal': 'halal', 'Vegan': 'vegan',
                     'Allergen-Safe': 'allergen', 'Eco-Friendly': 'eco'}

    max_contributors = 5
    for label, key in label_mapping.items():
        contributors = []
        for item in evidence:
            if item['found']:
                score = item['scores'].get(key, 0.5)
                # Invert allergen logic for contribution: high allergen score is BAD for Allergen-Safe
                if key == 'allergen':
                    score = 1.0 - score
                    
                contributors.append({
                    'ingredient': item['ingredient'],
                    'score': round(score, 3),
                    'impact': 'positive' if score > 0.6 else 'negative' if score < 0.4 else 'neutral'
                })

        # Sort by absolute distance from 0.5 (most impactful)
        contributors.sort(key=lambda x: abs(x['score'] - 0.5), reverse=True)
        api_response['top_contributors'][label] = contributors[:max_contributors]

    # KG evidence
    for item in evidence:
        if item['found']:
            api_response['kg_evidence'].append({
                'ingredient': item['ingredient'],
                'canonical_name': item['canonical_name'],
                'source': item['source'],
                'scores': item['scores'],
                'reasoning': item['reasoning']
            })

    # Overall confidence
    if predictions:
        avg_confidence = np.mean([p['confidence'] for p in predictions.values()])
        if avg_confidence > 0.7:
            api_response['confidence_level'] = 'high'
        elif avg_confidence < 0.4:
            api_response['confidence_level'] = 'low'

    return api_response
