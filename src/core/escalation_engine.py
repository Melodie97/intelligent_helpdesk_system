from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import json
from typing import Tuple, Optional
from .models import RequestCategory, ClassificationResult
from config.settings import Config

class EscalationEngine:
    def __init__(self):
        self.config = Config()
        self.categories = self._load_categories()
        self.embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        self.escalation_vectorstore = self._build_escalation_vectorstore()
    
    def _load_categories(self) -> dict:
        with open(self.config.categories_file, 'r') as f:
            return json.load(f)['categories']
    
    def _build_escalation_vectorstore(self):
        escalation_docs = [
            # Category-specific escalation triggers from categories.json
            Document(page_content="multiple failed resets account security concerns", metadata={'type': 'password_reset', 'category': 'password_reset', 'contact': 'it-support@techcorp.com'}),
            Document(page_content="unapproved software requests system compatibility issues", metadata={'type': 'software_installation', 'category': 'software_installation', 'contact': 'it-support@techcorp.com'}),
            Document(page_content="all hardware failures require escalation", metadata={'type': 'hardware_failure', 'category': 'hardware_failure', 'contact': 'hardware-support@techcorp.com'}),
            Document(page_content="network infrastructure issues multiple users affected", metadata={'type': 'network_connectivity', 'category': 'network_connectivity', 'contact': 'network-support@techcorp.com'}),
            Document(page_content="server configuration changes distribution list modifications", metadata={'type': 'email_configuration', 'category': 'email_configuration', 'contact': 'email-support@techcorp.com'}),
            Document(page_content="all security incidents require immediate escalation", metadata={'type': 'security_incident', 'category': 'security_incident', 'contact': 'security@techcorp.com'}),
            Document(page_content="policy clarification needed exception requests", metadata={'type': 'policy_question', 'category': 'policy_question', 'contact': 'it-support@techcorp.com'}),
            
            # Troubleshooting database escalation triggers
            Document(page_content="multiple failed reset attempts account lockout", metadata={'type': 'password_reset', 'category': 'password_reset', 'contact': 'security@techcorp.com'}),
            Document(page_content="performance issues persist after basic troubleshooting", metadata={'type': 'hardware_failure', 'category': 'hardware_failure', 'contact': 'hardware-support@techcorp.com'}),
            Document(page_content="unable to connect with any network or ethernet", metadata={'type': 'network_connectivity', 'category': 'network_connectivity', 'contact': 'network-support@techcorp.com'}),
            Document(page_content="email account configuration errors server connectivity issues", metadata={'type': 'email_configuration', 'category': 'email_configuration', 'contact': 'email-support@techcorp.com'}),
            Document(page_content="installation fails system compatibility requires admin privileges", metadata={'type': 'software_installation', 'category': 'software_installation', 'contact': 'software-support@techcorp.com'})
        ]
        return FAISS.from_documents(escalation_docs, self.embeddings)
    
    def should_escalate(self, request: str, classification: ClassificationResult) -> Tuple[bool, Optional[str]]:
        category_info = self.categories[classification.category.value]
        
        # Check category-specific escalation triggers
        escalation_triggers = category_info.get('escalation_triggers', [])
        
        # Always escalate certain categories
        if any('All' in trigger or 'immediate' in trigger.lower() for trigger in escalation_triggers):
            return True, f"Category {classification.category.value} requires automatic escalation"
        
        # Security incidents always escalate
        if classification.category == 'security_incident':
            return True, "Security incidents require immediate escalation"
        
        # Hardware failures always escalate
        if classification.category == 'hardware_failure':
            return True, "Hardware failures require escalation to hardware support"
        
        # Use vector similarity to detect category-specific escalation triggers
        similar_docs = self.escalation_vectorstore.similarity_search_with_score(request, k=3)
        for doc, score in similar_docs:
            if score < 0.8:  # High similarity threshold
                escalation_type = doc.metadata['type']
                doc_category = doc.metadata.get('category')
                
                # Only escalate if the trigger matches the classified category
                if doc_category == classification.category.value:
                    contact = doc.metadata.get('contact', 'it-support@techcorp.com')
                    if escalation_type == 'password_reset':
                        return True, f"Password reset escalation detected - Contact: {contact}"
                    elif escalation_type == 'software_installation':
                        return True, f"Software installation escalation detected - Contact: {contact}"
                    elif escalation_type == 'network_connectivity':
                        return True, f"Network connectivity escalation detected - Contact: {contact}"
                    elif escalation_type == 'email_configuration':
                        return True, f"Email configuration escalation detected - Contact: {contact}"
                    elif escalation_type == 'policy_question':
                        return True, f"Policy question escalation detected - Contact: {contact}"
                    elif escalation_type == 'hardware_failure':
                        return True, f"Hardware/performance escalation detected - Contact: {contact}"
        
        # Low confidence classification
        if classification.confidence < 0.3:
            return True, "Low confidence in classification - human review needed"
        
        return False, None