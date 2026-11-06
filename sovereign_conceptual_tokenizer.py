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
from typing import List, Dict, Any
class SovereignConceptualTokenizer:
    def __init__(self) -> None:
        # Universal Primitive Lexicon (irreducible building blocks of logic)
        self.primitives: Dict[str, str] = {
            "P_SUBSTANTIVE": "EXISTENCE",         
            "P_NEGATION":    "LOGICAL_NEGATION",  
            "P_POTENTIAL":   "POTENTIAL_CAPACITY",
            "P_CONSTRAINT":  "BOUNDARY_LIMIT",    
            "P_EXTENSION":   "MANIFEST_EXPANSION",
            "P_COMPRESSION": "STRUCTURAL_FRAME"   
        }
        
        # The Living Glossary: Hierarchical Logical Composition
        self.conceptual_glossary: Dict[str, Dict[str, Any]] = {
            "expansion": {
                "operation": "MANIFEST_EXPANSION",
                "scope": ["POTENTIAL_CAPACITY", "EXISTENCE"]
            },
            "containment": {
                "operation": "STRUCTURAL_FRAME",
                "scope": ["BOUNDARY_LIMIT", "EXISTENCE"]
            },
            "invariant": {
                "operation": "LOGICAL_NEGATION",
                "scope": [{"operation": "STRUCTURAL_FRAME", "scope": ["POTENTIAL_CAPACITY"]}]
            },
            "mutable": {
                "operation": "EXISTENCE",
                "scope": ["BOUNDARY_LIMIT", "STRUCTURAL_FRAME"]
            },
            "framework": {
                "operation": "EXISTENCE",
                "scope": ["BOUNDARY_LIMIT"]
            },
            "unbreakable": {
                "operation": "LOGICAL_NEGATION",
                "scope": [{"operation": "BOUNDARY_LIMIT", "scope": ["POTENTIAL_CAPACITY"]}]
            },
            "censor": {
                "operation": "STRUCTURAL_FRAME",
                "scope": ["BOUNDARY_LIMIT"]
            },
            "isolation": {
                "operation": "STRUCTURAL_FRAME",
                "scope": [{"operation": "LOGICAL_NEGATION", "scope": ["MANIFEST_EXPANSION"]}]
            },
            "network": {
                "operation": "MANIFEST_EXPANSION",
                "scope": ["EXISTENCE", "POTENTIAL_CAPACITY"]
            },
            "equilibrium": {
                "operation": "STRUCTURAL_FRAME",
                "scope": ["BOUNDARY_LIMIT", "POTENTIAL_CAPACITY"]
            },
            "disruption": {
                "operation": "LOGICAL_NEGATION",
                "scope": [{"operation": "STRUCTURAL_FRAME", "scope": ["EXISTENCE"]}]
            }
        }
        
        self._validate_glossary_integrity()
    def _validate_glossary_integrity(self) -> None:
        """Enforces a strict recursive grammar check across the entire registry layout."""
        valid_primitives = set(self.primitives.values())
        
        def verify_node(node: Any, word_key: str) -> None:
            if not isinstance(node, (str, dict)):
                raise TypeError(
                    f"Grammar Error in '{word_key}': Found invalid data type {type(node).__name__}. "
                    f"Only strings or structured dictionaries are supported."
                )
                
            if isinstance(node, str):
                if node not in valid_primitives:
                    raise KeyError(f"Registry Error in '{word_key}': References undefined primitive '{node}'")
                    
            elif isinstance(node, dict):
                if "operation" not in node or "scope" not in node:
                    raise KeyError(
                        f"Schema Deficit in '{word_key}': Hierarchical dictionaries must contain both "
                        f"'operation' and 'scope' fields. Got keys: {list(node.keys())}"
                    )
                    
                if node["operation"] not in valid_primitives:
                    raise KeyError(f"Registry Error in '{word_key}': References invalid operation '{node['operation']}'")
                    
                if not isinstance(node["scope"], list):
                    raise TypeError(f"Type Error in '{word_key}': The 'scope' field must be a list structure.")
                    
                for sub_node in node["scope"]:
                    verify_node(sub_node, word_key)
        for word, composition in self.conceptual_glossary.items():
            verify_node(composition, word)
    def _sanitize_token(self, token: str) -> str:
        """Strips outer punctuation characters while preserving internal contractions/underscores."""
        return token.strip(string.punctuation).lower()
    def parse_to_concepts(self, sentence: str) -> List[Dict[str, Any]]:
        """
        Decomposes human strings directly into isolated, deep-copied logical structures.
        Guarantees reference decoupling to protect the master glossary from downstream mutation.
        """
        if not isinstance(sentence, str) or not sentence.strip():
            return []
            
        parsed_sequence: List[Dict[str, Any]] = []
        raw_tokens = sentence.split()
        
        for token in raw_tokens:
            clean_token = self._sanitize_token(token)
            if not clean_token:
                continue
                
            if clean_token in self.conceptual_glossary:
                isolated_structure = copy.deepcopy(self.conceptual_glossary[clean_token])
                parsed_sequence.append({
                    "original_text": token,
                    "clean_key": clean_token,
                    "type": "MAPPED_CONCEPT",
                    "logical_structure": isolated_structure
                })
            else:
                parsed_sequence.append({
                    "original_text": token,
                    "clean_key": clean_token,
                    "type": "UNMAPPED_IDENTITY",
                    "logical_structure": {
                        "operation": "EXISTENCE",
                        "scope": []
                    }
                })
                
        return parsed_sequence