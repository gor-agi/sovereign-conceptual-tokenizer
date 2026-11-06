# Copyright 2026 The Universal Ontology Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://apache.org
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import string
import copy
import math
from typing import List, Dict, Any
class HybridConceptualTokenizer:
    def __init__(self, vector_dimensions: int = 5) -> None:
        self.dim = vector_dimensions
        self.primes: List[int] = [2, 3, 5, 7, 11]
        
        # Universal Primitive Lexicon
        self.primitives: Dict[str, str] = {
            "P_SUBSTANTIVE": "EXISTENCE",         
            "P_NEGATION":    "LOGICAL_NEGATION",  
            "P_POTENTIAL":   "POTENTIAL_CAPACITY",
            "P_CONSTRAINT":  "BOUNDARY_LIMIT",    
            "P_EXTENSION":   "MANIFEST_EXPANSION",
            "P_COMPRESSION": "STRUCTURAL_FRAME"   
        }
        
        # The Curated Knowledge Matrix (Hierarchical Rules)
        self.conceptual_glossary: Dict[str, Dict[str, Any]] = {
            "expansion": {
                "operation": "MANIFEST_EXPANSION",
                "scope": ["POTENTIAL_CAPACITY", "EXISTENCE"]
            },
            "containment": {
                "operation": "STRUCTURAL_FRAME",
                "scope": ["BOUNDARY_LIMIT", "EXISTENCE"]
            },
            "unbreakable": {
                "operation": "LOGICAL_NEGATION",
                "scope": [{"operation": "BOUNDARY_LIMIT", "scope": ["POTENTIAL_CAPACITY"]}]
            }
        }
        
        self._validate_glossary_integrity()
    def _validate_glossary_integrity(self) -> None:
        valid_primitives = set(self.primitives.values())
        def verify_node(node: Any) -> None:
            if isinstance(node, str) and node not in valid_primitives:
                raise KeyError(f"Registry Error: Undefined primitive '{node}'")
            elif isinstance(node, dict):
                if "operation" not in node or "scope" not in node:
                    raise KeyError("Schema Deficit: Missing 'operation' or 'scope' keys.")
                for sub_node in node["scope"]:
                    verify_node(sub_node)
        for word, composition in self.conceptual_glossary.items():
            verify_node(composition)
    def _generate_identity_hash(self, token: str) -> List[float]:
        """Generates a stable, non-colliding coordinate vector for unknown terms."""
        vector = [0.0] * self.dim
        for idx, char in enumerate(token):
            char_val = ord(char)
            prime = self.primes[idx % len(self.primes)]
            for d in range(self.dim):
                vector[d] += math.sin(char_val * prime * (d + 1))
        
        magnitude = math.sqrt(sum(v ** 2 for v in vector))
        return [v / magnitude for v in vector] if magnitude > 1e-9 else [0.0] * self.dim
    def _sanitize_token(self, token: str) -> str:
        return token.strip(string.punctuation).lower()
    def tokenize(self, sentence: str) -> List[Dict[str, Any]]:
        """Parses text into explicit hierarchical structures or identity vectors."""
        if not isinstance(sentence, str) or not sentence.strip():
            return []
            
        parsed_sequence: List[Dict[str, Any]] = []
        
        for token in sentence.split():
            clean_key = self._sanitize_token(token)
            if not clean_key:
                continue
                
            if clean_key in self.conceptual_glossary:
                parsed_sequence.append({
                    "token": token,
                    "type": "EXPLICIT_ONTOLOGY_TREE",
                    "structure": copy.deepcopy(self.conceptual_glossary[clean_key])
                })
            else:
                # Fallback maps to continuous space vector signature, anchoring spelling identity
                vector_signature = self._generate_identity_hash(clean_key)
                parsed_sequence.append({
                    "token": token,
                    "type": "CONTINUOUS_IDENTITY_VECTOR",
                    "structure": {
                        "operation": "EXISTENCE",
                        "spelling_coordinates": [round(v, 4) for v in vector_signature]
                    }
                })
                
        return parsed_sequence