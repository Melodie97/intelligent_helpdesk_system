from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
from ..models.state import HelpDeskState, ClassificationResult, RequestCategory

class ClassifierAgent:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        self.categories = self._load_categories()
        self.category_embeddings = None
        self._train()
    
    def _load_categories(self):
        categories_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'categories.json')
        with open(categories_file, 'r') as f:
            return json.load(f)['categories']
    
    def _train(self):
        category_texts = []
        self.category_names = []
        
        for cat_name, cat_info in self.categories.items():
            text = cat_info['description']
            category_texts.append(text)
            self.category_names.append(cat_name)
        
        self.category_embeddings = self.embeddings.embed_documents(category_texts)
    
    def classify(self, state: HelpDeskState) -> HelpDeskState:
        request = state["request"]
        request_embedding = self.embeddings.embed_query(request)
        similarities = cosine_similarity([request_embedding], self.category_embeddings)[0]
        
        best_match_idx = np.argmax(similarities)
        confidence = similarities[best_match_idx]
        
        category = RequestCategory(self.category_names[best_match_idx])
        classification = ClassificationResult(category=category, confidence=float(confidence))
        
        state["classification"] = classification
        state["next_action"] = "retrieve_knowledge"
        
        return state