import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModel
import networkx as nx
import numpy as np
from typing import Dict, List, Tuple, Any

class IngredientKnowledgeGraph:
    """Knowledge Graph for ingredient reasoning"""

    def __init__(self, knowledge_base: Dict):
        self.kb = knowledge_base
        self.graph = nx.DiGraph()
        self._build_graph()
        self._build_synonym_map()

    def _build_graph(self):
        for ingredient, props in self.kb.items():
            self.graph.add_node(ingredient, node_type='ingredient', **props)

            chem_class = props.get('chemical_class', 'unknown')
            if not self.graph.has_node(chem_class):
                self.graph.add_node(chem_class, node_type='chemical_class')
            self.graph.add_edge(ingredient, chem_class, relation='belongs_to')

            source = props.get('source', 'unknown')
            if not self.graph.has_node(source):
                self.graph.add_node(source, node_type='source_type')
            self.graph.add_edge(ingredient, source, relation='derived_from')

    def _build_synonym_map(self):
        self.synonym_map = {}
        for ingredient, props in self.kb.items():
            self.synonym_map[ingredient.lower()] = ingredient
            for syn in props.get('synonyms', []):
                self.synonym_map[syn.lower()] = ingredient

    def lookup(self, ingredient_text: str) -> Dict:
        """Lookup ingredient in KB"""
        ingredient_lower = ingredient_text.lower().strip()

        if ingredient_lower in self.synonym_map:
            canonical = self.synonym_map[ingredient_lower]
            return {
                'found': True,
                'canonical_name': canonical,
                'properties': self.kb[canonical]
            }

        # Partial match
        for known_ing in self.synonym_map.keys():
            if known_ing in ingredient_lower or ingredient_lower in known_ing:
                canonical = self.synonym_map[known_ing]
                return {
                    'found': True,
                    'canonical_name': canonical,
                    'properties': self.kb[canonical]
                }

        return {
            'found': False,
            'canonical_name': None,
            'properties': self._get_default_properties()
        }

    def _get_default_properties(self) -> Dict:
        return {
            'chemical_class': 'unknown',
            'source': 'unknown',
            'halal': 0.5,
            'vegan': 0.5,
            'allergen': 0.5,
            'eco': 0.5,
            'reasoning': 'Unknown ingredient'
        }

    def extract_features(self, ingredient_list: List[str]) -> np.ndarray:
        """Extract KG features: [halal, vegan, allergen, eco,
                                  num_animal, num_plant, num_synthetic, num_unknown, confidence]"""
        features = np.zeros(9)
        num_ingredients = len(ingredient_list)

        if num_ingredients == 0:
            return features

        found_count = 0
        for ing in ingredient_list:
            result = self.lookup(ing)
            props = result['properties']

            if result['found']:
                found_count += 1

            # Aggregate scores
            features[0] += props.get('halal', 0.5)
            features[1] += props.get('vegan', 0.5)
            features[2] += props.get('allergen', 0.5)
            features[3] += props.get('eco', 0.5)

            # Count sources
            source = props.get('source', 'unknown')
            if source == 'animal':
                features[4] += 1
            elif source == 'plant':
                features[5] += 1
            elif source == 'synthetic':
                features[6] += 1
            else:
                features[7] += 1

        # Normalize
        features[:4] /= num_ingredients
        features[4:8] /= num_ingredients
        features[8] = found_count / num_ingredients

        return features

class HybridCosmeticClassifier(nn.Module):
    """Enhanced Architecture: BERT + Knowledge Graph with Multi-Head Attention Fusion"""

    def __init__(self, transformer_name='bert-base-uncased',
                 kg_feature_dim=9, num_labels=4, dropout=0.3):
        super().__init__()

        # BERT encoder
        self.transformer = AutoModel.from_pretrained(transformer_name)
        self.transformer_dim = self.transformer.config.hidden_size

        # Enhanced knowledge graph encoder
        self.kg_encoder = nn.Sequential(
            nn.Linear(kg_feature_dim, 128),
            nn.LayerNorm(128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, 256),
            nn.LayerNorm(256),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(256, 256),
            nn.LayerNorm(256),
            nn.ReLU(),
            nn.Dropout(dropout)
        )

        # Projection layer
        self.kg_projection = nn.Linear(256, self.transformer_dim)

        # Multi-head attention
        self.fusion_attention = nn.MultiheadAttention(
            embed_dim=self.transformer_dim,
            num_heads=8,
            dropout=dropout,
            batch_first=True
        )

        # Enhanced fusion layer
        fusion_dim = self.transformer_dim + 256
        self.fusion = nn.Sequential(
            nn.Linear(fusion_dim, 768),
            nn.LayerNorm(768),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(768, 512),
            nn.LayerNorm(512),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(512, 384),
            nn.LayerNorm(384),
            nn.ReLU(),
            nn.Dropout(dropout)
        )

        # Multi-label head
        self.classifier = nn.Sequential(
            nn.Linear(384, 128),
            nn.LayerNorm(128),
            nn.ReLU(),
            nn.Dropout(dropout / 2),
            nn.Linear(128, num_labels)
        )

        # Attention weights
        self.text_attention = nn.Linear(self.transformer_dim, 1)
        self.kg_attention = nn.Linear(256, 1)

    def forward(self, input_ids, attention_mask, kg_features, return_explanations=False):
        # Encode text
        transformer_output = self.transformer(
            input_ids=input_ids,
            attention_mask=attention_mask,
            output_attentions=return_explanations
        )
        text_embedding = transformer_output.last_hidden_state[:, 0, :]  # [CLS]

        # Encode KG features
        kg_embedding = self.kg_encoder(kg_features)

        # Multi-head attention fusion
        text_unsqueezed = text_embedding.unsqueeze(1)  # [batch, 1, dim]
        kg_projected = self.kg_projection(kg_embedding)
        kg_proj_unsqueezed = kg_projected.unsqueeze(1)

        attended_features, fusion_attention_weights = self.fusion_attention(
            text_unsqueezed, kg_proj_unsqueezed, kg_proj_unsqueezed
        )
        attended_features = attended_features.squeeze(1)

        # Weighted fusion
        text_attn = torch.sigmoid(self.text_attention(text_embedding))
        kg_attn = torch.sigmoid(self.kg_attention(kg_embedding))

        attn_sum = text_attn + kg_attn + 1e-8
        text_weight = text_attn / attn_sum
        kg_weight = kg_attn / attn_sum

        text_weighted = attended_features * text_weight
        kg_weighted = kg_embedding * kg_weight

        # Concatenate and fuse
        combined = torch.cat([text_weighted, kg_weighted], dim=1)
        fused = self.fusion(combined)

        # Classify
        logits = self.classifier(fused)
        
        if return_explanations:
            explanations = {
                'text_weight': text_weight.detach(),
                'kg_weight': kg_weight.detach(),
                'fusion_attention': fusion_attention_weights.detach(),
                'bert_attentions': transformer_output.attentions,
                'kg_features': kg_features.detach(),
                'kg_embedding': kg_embedding.detach()
            }
            return logits, explanations

        return logits
