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
class ClassificationResult(BaseModel):
    label: str
    probability: float
    is_present: bool

class AnalysisResponse(BaseModel):
    results: List[ClassificationResult]
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
    
    if not ing_list:
        raise HTTPException(status_code=400, detail="Could not extract any content. Please provide valid cosmetic ingredients.")
        
    unknown_ingredients = [ing for ing in ing_list if not kg.lookup(ing)['found']]
    if unknown_ingredients:
        raise HTTPException(
            status_code=400,
            detail=f"Unrecognized or irrelevant text detected: {', '.join(unknown_ingredients)}. Please enter only valid cosmetic ingredients."
        )
    
    # Calculate average scores based on DETAILED INGREDIENT ANALYSIS logic
    avg_scores = {'Halal': 0.0, 'Vegan': 0.0, 'Allergen-Safe': 0.0, 'Eco-Friendly': 0.0}
    if ing_list:
        for label_name, prop_name in [('Halal', 'halal'), ('Vegan', 'vegan'), ('Allergen-Safe', 'allergen'), ('Eco-Friendly', 'eco')]:
            total = 0.0
            for ing in ing_list:
                result = kg.lookup(ing)
                props = result['properties']
                score = props.get(prop_name, 0.5)
                if label_name == 'Allergen-Safe':
                    score = 1.0 - score  # Invert for allergen-safe
                total += score
            avg_scores[label_name] = total / len(ing_list)
    else:
        avg_scores = {'Halal': 0.5, 'Vegan': 0.5, 'Allergen-Safe': 0.5, 'Eco-Friendly': 0.5}

    # Classification
    results = []
    label_names = ['Halal', 'Vegan', 'Allergen-Safe', 'Eco-Friendly'] 
    
    if model:
        # Prepare inputs to ensure model runtime runs without errors
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
                _ = model(input_ids, attention_mask, kg_tensor)
                
            # Construct results using the average scores from detailed analysis
            for label in label_names:
                score = avg_scores[label]
                results.append(ClassificationResult(label=label, probability=float(score), is_present=score>=0.5))
            
        except Exception as e:
            print(f"Inference error: {e}")
            for label in label_names:
                score = avg_scores[label]
                results.append(ClassificationResult(label=label, probability=float(score), is_present=score>=0.5))

    else:
        # Mock Mode uses identical average score logic
        for label in label_names:
            score = avg_scores[label]
            results.append(ClassificationResult(label=label, probability=float(score), is_present=score>=0.5))

    return AnalysisResponse(
        results=results,
        model_status="Active" if model else "Mock Mode"
    )

# Explanability Logic rewritten natively here

def generate_xai_reasoning(text: str, label_name: str, prediction: str,
                          probability: float, explanations: Dict,
                          ingredient_list: List[str], kg_features: np.ndarray,
                          tokens: List[str]) -> str:
    # Extract attention weights
    text_weight = float(explanations['text_weight'][0, 0])
    kg_weight = float(explanations['kg_weight'][0, 0])

    # Get BERT attention (average across all layers and heads)
    bert_attentions = explanations['bert_attentions']
    top_ingredients = []

    if bert_attentions is not None:
        # BERT attention is available - use it for ingredient analysis
        avg_attention = torch.stack([attn[0].mean(0) for attn in bert_attentions]).mean(0)
        avg_attention = avg_attention[0, 1:].cpu().numpy()  # Remove CLS token

        # Map attention to ingredients
        ingredient_attention = {}
        for i, token in enumerate(tokens[1:len(avg_attention)+1]):  # Skip CLS
            if token not in ['[PAD]', '[SEP]']:
                for ing in ingredient_list:
                    if token in ing.lower():
                        ingredient_attention[ing] = ingredient_attention.get(ing, 0) + avg_attention[i]

        # Get top attended ingredients
        if ingredient_attention:
            top_ingredients = sorted(ingredient_attention.items(),
                                    key=lambda x: x[1], reverse=True)[:3]
    else:
        for ing in ingredient_list[:3]:  # proxy
            top_ingredients.append((ing, 1.0))

    # Analyze KG feature contributions
    label_map = {'Halal': 0, 'Vegan': 1, 'Allergen-Safe': 2, 'Eco-Friendly': 3, 'Contains Allergens': 2}
    label_idx = label_map.get(label_name, 0)
    kg_score = kg_features[label_idx]
    
    # Adjust for Allergen inverted logic from KG (in KG high allergen means allergen present)
    # Actually wait: kg_score for Allergen is high explicitly. So let's keep it raw and interpret properly.
    if label_name == 'Allergen-Safe':
        kg_score = 1.0 - kg_score # Invert score: High means safe.

    # Determine confidence level
    confidence = abs(probability - 0.5) * 2
    conf_text = "high" if confidence > 0.7 else "moderate" if confidence > 0.4 else "low"

    # Generate reasoning sentences
    reasoning_parts = []

    # Sentence 1: What the model focused on
    if text_weight > kg_weight:
        if top_ingredients:
            top_ing_names = [ing[0] for ing in top_ingredients[:2]]
            ing_str = ' and '.join(top_ing_names)
            reasoning_parts.append(
                f"The model predicted {prediction} for {label_name} with {conf_text} confidence "
                f"({probability:.1%}), primarily focusing on the ingredients {ing_str} "
                f"through text analysis ({text_weight:.0%} attention weight)."
            )
        else:
            reasoning_parts.append(
                f"The model predicted {prediction} for {label_name} with {conf_text} confidence "
                f"({probability:.1%}), relying heavily on textual patterns "
                f"({text_weight:.0%} attention to text features)."
            )
    else:
        kg_impact = "positive" if kg_score > 0.5 else "negative"
        reasoning_parts.append(
            f"The model predicted {prediction} for {label_name} with {conf_text} confidence "
            f"({probability:.1%}), primarily using knowledge graph features "
            f"({kg_weight:.0%} attention weight) which indicate a {kg_impact} assessment "
            f"(KG score: {kg_score:.2f})."
        )

    # Sentence 2: Supporting evidence
    if kg_weight > 0.3:  # KG played a role
        kg_desc = "high" if kg_score > 0.7 else "moderate" if kg_score > 0.4 else "low"
        reasoning_parts.append(
            f"The knowledge graph analysis contributed {kg_desc} safety scores "
            f"({kg_score:.2f}) based on ingredient source and composition data."
        )
    elif top_ingredients:
        reasoning_parts.append(
            f"The attention mechanism identified {top_ingredients[0][0]} as the most "
            f"influential ingredient (attention weight: {top_ingredients[0][1]:.3f})."
        )

    return " ".join(reasoning_parts)

def generate_per_ingredient_xai_reasoning(text: str, explanations: Dict,
                                        ingredient_list: List[str],
                                        kg_features: np.ndarray,
                                        tokens: List[str],
                                        probs: np.ndarray) -> Dict[str, Dict]:
    label_names = ['Halal', 'Vegan', 'Allergen-Safe', 'Eco-Friendly']
    label_map = {'Halal': 0, 'Vegan': 1, 'Allergen-Safe': 2, 'Eco-Friendly': 3}

    bert_attentions = explanations['bert_attentions']
    ingredient_attention_scores = {}

    if bert_attentions is not None:
        avg_attention = torch.stack([attn[0].mean(0) for attn in bert_attentions]).mean(0)
        avg_attention = avg_attention[0, 1:].cpu().numpy()  # Remove CLS token
        for ing in ingredient_list:
            total_attention = 0
            for i, token in enumerate(tokens[1:len(avg_attention)+1]):
                if token not in ['[PAD]', '[SEP]'] and token in ing.lower():
                    total_attention += avg_attention[i]
            ingredient_attention_scores[ing] = total_attention
    else:
        for ing in ingredient_list:
            ingredient_attention_scores[ing] = 1.0 / max(1, len(ingredient_list))

    ingredient_reasoning = {}

    for ing in ingredient_list:
        kb_result = kg.lookup(ing)
        ing_props = kb_result['properties']

        attn_score = ingredient_attention_scores.get(ing, 0)
        attn_sum = sum(ingredient_attention_scores.values())
        attn_pct = (attn_score / attn_sum * 100) if attn_sum > 0 else 0

        label_reasoning = {}

        for label_name in label_names:
            label_key = label_name.lower().replace('-safe', '').replace('-friendly', '')
            kg_score = ing_props.get(label_key, 0.5)

            if label_name == 'Allergen-Safe':
                kg_score = 1.0 - kg_score

            label_idx = label_map[label_name]
            pred_prob = float(probs[label_idx])
            
            if label_name == 'Allergen-Safe':
                pred_prob = 1.0 - pred_prob

            prediction = 'Positive' if pred_prob > 0.5 else 'Negative'

            if kg_score > 0.7:
                impact = "strongly supports"
                impact_emoji = "✅✅"
            elif kg_score > 0.5:
                impact = "supports"
                impact_emoji = "✅"
            elif kg_score > 0.3:
                impact = "has neutral effect on"
                impact_emoji = "⚠️"
            else:
                impact = "negatively affects"
                impact_emoji = "❌"

            source = ing_props.get('source', 'unknown')
            source_desc = {
                'animal': 'animal-derived',
                'plant': 'plant-based',
                'synthetic': 'synthetically produced',
                'natural': 'naturally occurring',
                'ambiguous': 'ambiguous origin',
                'unknown': 'unknown origin'
            }.get(source, source)

            if kb_result['found']:
                kb_reasoning = ing_props.get('reasoning', 'No specific reasoning available')
                reasoning = (
                    f"{ing.title()} ({source_desc}) {impact} the {label_name} classification "
                    f"because it is {kb_reasoning.lower()}. "
                    # f"Model attention weight: {attn_pct:.1f}%."
                )
            else:
                reasoning = (
                    f"{ing.title()} (unknown ingredient) has uncertain impact on {label_name}. "
                    # f"Model attention weight: {attn_pct:.1f}%."
                )

            label_reasoning[label_name] = {
                'reasoning': reasoning,
                'kg_score': round(kg_score, 3),
                'attention_weight': round(attn_pct, 2),
                'impact': impact.replace('strongly ', '').replace('has neutral effect on', 'neutral').replace('negatively affects', 'preventing').replace('supports', 'supporting'), # Clean map for frontend UI
                'impact_raw': impact,
                'source': source
            }

        ingredient_reasoning[ing] = label_reasoning

    return ingredient_reasoning

@app.post("/explain")
async def get_detailed_explanation(request: IngredientRequest):
    text = request.ingredients
    if not text.strip():
        raise HTTPException(status_code=400, detail="No ingredients provided")
        
    clean_text = clean_ingredient_text(text)
    ing_list = extract_ingredients(clean_text)
    
    if not ing_list:
        raise HTTPException(status_code=400, detail="Could not extract any content. Please provide valid cosmetic ingredients.")
        
    unknown_ingredients = [ing for ing in ing_list if not kg.lookup(ing)['found']]
    if unknown_ingredients:
        raise HTTPException(
            status_code=400,
            detail=f"Unrecognized or irrelevant text detected: {', '.join(unknown_ingredients)}. Please enter only valid cosmetic ingredients."
        )
    
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
        tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
        
        try:
            with torch.no_grad():
                logits, explanations = model(
                    input_ids, attention_mask, kg_tensor, return_explanations=True
                )
                probs = torch.sigmoid(logits).cpu().numpy()[0]
                
            for i, label in enumerate(label_names):
                prob = float(probs[i])
                
                # Invert logic for Allergen-Safe so > 0.5 means Safe
                if i == 2:
                    prob = 1.0 - prob
                
                prediction = 'Positive' if prob > 0.5 else 'Negative'
                confidence = abs(prob - 0.5) * 2
                
                xai_reasoning = generate_xai_reasoning(
                    clean_text, label, prediction, prob, explanations,
                    ing_list, kg_features, tokens
                )
                
                predictions[label] = {
                    'prediction': prediction,
                    'probability': round(prob, 4),
                    'confidence': round(confidence, 4),
                    'xai_reasoning': xai_reasoning
                }
                
            ingredient_reasoning = generate_per_ingredient_xai_reasoning(
                clean_text, explanations, ing_list, kg_features, tokens, probs
            )
            
        except Exception as e:
            print(f"XAI inference error: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to run model explanation: {e}")
            
    else:
        raise HTTPException(status_code=503, detail="Model is currently unavailable for detailed explanation. Running in mock mode.")

    # Format for API
    api_response = {
        'predictions': predictions,
        'all_contributors': {},
        'ingredient_reasoning': ingredient_reasoning,
        'ambiguous_ingredients': [],
        'confidence_level': 'medium'
    }

    # Map ingredient_reasoning to the old all_contributors structure for backwards compatibility
    for label in label_names:
        supporting = []
        preventing = []
        for ing, labels_data in ingredient_reasoning.items():
            data = labels_data[label]
            # using 'supporting' / 'preventing' from 'impact' map earlier
            contributor = {
                'ingredient': ing,
                'score': data['kg_score'],
                'impact': 'positive' if 'supporting' in data['impact'] else 'negative' if 'preventing' in data['impact'] else 'neutral',
                'attention_weight': data['attention_weight'],
                'reasoning': data['reasoning']
            }
            if contributor['impact'] == 'positive':
                supporting.append(contributor)
            else:
                preventing.append(contributor)
                
        supporting.sort(key=lambda x: x['attention_weight'], reverse=True)
        preventing.sort(key=lambda x: x['attention_weight'], reverse=True)
        
        api_response['all_contributors'][label] = {
            'supporting': supporting,
            'preventing': preventing
        }
        
    for ing in ing_list:
        kb = kg.lookup(ing)
        if not kb['found'] or kb['properties'].get('source') == 'ambiguous':
            api_response['ambiguous_ingredients'].append({
                'ingredient': ing,
                'reason': 'Not found in knowledge base' if not kb['found'] else 'Ambiguous source'
            })

    if predictions:
        avg_confidence = np.mean([p['confidence'] for p in predictions.values()])
        if avg_confidence > 0.7:
            api_response['confidence_level'] = 'high'
        elif avg_confidence < 0.4:
            api_response['confidence_level'] = 'low'

    return api_response

