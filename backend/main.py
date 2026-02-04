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
            state_dict = torch.load(MODEL_PATH, map_location=device)
            model.load_state_dict(state_dict)
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
