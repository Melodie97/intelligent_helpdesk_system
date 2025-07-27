from ..workflows.helpdesk_workflow import HelpDeskWorkflow
from .state import HelpDeskRequest, HelpDeskResponse, ClassificationResult, RequestCategory

class HelpDeskSystem:
    def __init__(self):
        self.multi_agent_workflow = HelpDeskWorkflow()
    
    def process_request(self, request: HelpDeskRequest) -> HelpDeskResponse:
        # Process request through multi-agent workflow
        result = self.multi_agent_workflow.process_request(
            request=request.request,
            user_id=request.user_id
        )
        
        # Convert multi-agent result to original response format
        return HelpDeskResponse(
            classification=result['classification'],
            response=result['response'],
            knowledge_items=result['knowledge_items'],
            escalate=result['escalate'],
            escalation_reason=result['escalation_reason']
        )