from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import json
import os
from ..models.state import HelpDeskState

class EscalationAgent:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        self.categories = self._load_categories()
        self.escalation_vectorstore = self._build_escalation_vectorstore()
    
    def _load_categories(self):
        categories_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'categories.json')
        with open(categories_file, 'r') as f:
            return json.load(f)['categories']
    
    def _build_escalation_vectorstore(self):
        escalation_docs = [
            Document(page_content="multiple failed resets account security concerns", 
                    metadata={'type': 'password_reset', 'category': 'password_reset'}),
            Document(page_content="unapproved software requests system compatibility issues", 
                    metadata={'type': 'software_installation', 'category': 'software_installation'}),
            Document(page_content="all hardware failures require escalation", 
                    metadata={'type': 'hardware_failure', 'category': 'hardware_failure'}),
            Document(page_content="network infrastructure issues multiple users affected", 
                    metadata={'type': 'network_connectivity', 'category': 'network_connectivity'}),
            Document(page_content="server configuration changes distribution list modifications", 
                    metadata={'type': 'email_configuration', 'category': 'email_configuration'}),
            Document(page_content="all security incidents require immediate escalation", 
                    metadata={'type': 'security_incident', 'category': 'security_incident'}),
            Document(page_content="policy clarification needed exception requests", 
                    metadata={'type': 'policy_question', 'category': 'policy_question'})
        ]
        return FAISS.from_documents(escalation_docs, self.embeddings)
    
    def check_escalation(self, state: HelpDeskState) -> HelpDeskState:
        request = state["request"]
        classification = state["classification"]
        
        # Always escalate certain categories
        if classification.category in ['security_incident', 'hardware_failure']:
            state["escalate"] = True
            state["escalation_reason"] = f"{classification.category.value} requires automatic escalation"
            state["next_action"] = "generate_response"
            return state
        
        # Check vector similarity for escalation triggers
        similar_docs = self.escalation_vectorstore.similarity_search_with_score(request, k=3)
        for doc, score in similar_docs:
            if score < 0.8:
                doc_category = doc.metadata.get('category')
                if doc_category == classification.category.value:
                    escalation_type = doc.metadata['type']
                    state["escalate"] = True
                    state["escalation_reason"] = f"{escalation_type.replace('_', ' ').title()} escalation detected"
                    state["next_action"] = "generate_response"
                    return state
        
        # Low confidence classification
        if classification.confidence < 0.3:
            state["escalate"] = True
            state["escalation_reason"] = "Low confidence in classification - human review needed"
            state["next_action"] = "generate_response"
            return state
        
        state["escalate"] = False
        state["escalation_reason"] = None
        state["next_action"] = "generate_response"
        
        return state