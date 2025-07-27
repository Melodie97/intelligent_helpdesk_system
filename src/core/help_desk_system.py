from .classifier import RequestClassifier
from .knowledge_retriever import KnowledgeRetriever
from .escalation_engine import EscalationEngine
from ..llm.response_generator import ResponseGenerator
from .models import HelpDeskRequest, HelpDeskResponse

class HelpDeskSystem:
    def __init__(self):
        self.classifier = RequestClassifier()
        self.knowledge_retriever = KnowledgeRetriever()
        self.response_generator = ResponseGenerator()
        self.escalation_engine = EscalationEngine()
    
    def process_request(self, request: HelpDeskRequest) -> HelpDeskResponse:
        # Step 1: Classify the request
        classification = self.classifier.classify(request.request)
        
        # Step 2: Retrieve relevant knowledge
        knowledge_items = self.knowledge_retriever.retrieve(
            request.request, 
            classification.category,
            top_k=3
        )
        
        # Step 3: Check if escalation is needed
        should_escalate, escalation_reason = self.escalation_engine.should_escalate(
            request.request, 
            classification
        )
        
        # Step 4: Generate response
        if should_escalate:
            response_text = f"This request has been escalated to our support team. {escalation_reason or ''} You will receive a response within the next business hour."
        else:
            response_text = self.response_generator.generate_response(
                request.request,
                classification.category,
                knowledge_items
            )
        
        return HelpDeskResponse(
            classification=classification,
            response=response_text,
            knowledge_items=knowledge_items,
            escalate=should_escalate,
            escalation_reason=escalation_reason
        )