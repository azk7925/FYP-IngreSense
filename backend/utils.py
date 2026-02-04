import re
import pandas as pd
from typing import List, Union

def clean_ingredient_text(text: str) -> str:
    """Clean and normalize text"""
    if pd.isna(text) or text is None:
        return ""
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9,\s\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_ingredients(text: str) -> List[str]:
    """Split into individual ingredients"""
    if not text:
        return []
    ingredients = re.split(r'[,;]', text)
    return [ing.strip() for ing in ingredients if ing.strip()]

def normalize_label(value) -> int:
    """Convert labels to binary"""
    if pd.isna(value) or value is None:
        return 0
    if isinstance(value, str):
        value = value.lower().strip()
        # Positive labels
        if value in ['yes', 'true', '1', 'safe', 'halal', 'vegan', 'eco-friendly']:
            return 1
        # Negative labels (everything else is 0, including "needs verification")
        else:
            return 0
    # For numeric values
    try:
        return 1 if float(value) > 0.5 else 0
    except:
        return 0
