from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .models import RequestCategory, ClassificationResult
from config.settings import Config
import json

class RequestClassifier:
    def __init__(self):
        self.config = Config()
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.categories = self._load_categories()
        self.category_embeddings = None
        self._train()
    
    def _load_categories(self):
        with open(self.config.categories_file, 'r') as f:
            return json.load(f)['categories']
    
    def _train(self):
        category_texts = []
        self.category_names = []
        
        for cat_name, cat_info in self.categories.items():
            text = cat_info['description']
            category_texts.append(text)
            self.category_names.append(cat_name)
        
        self.category_embeddings = self.model.encode(category_texts)
    
    def classify(self, request: str) -> ClassificationResult:
        request_embedding = self.model.encode([request])
        similarities = cosine_similarity(request_embedding, self.category_embeddings)[0]
        
        best_match_idx = np.argmax(similarities)
        confidence = similarities[best_match_idx]
        
        category = RequestCategory(self.category_names[best_match_idx])
        return ClassificationResult(category=category, confidence=float(confidence))