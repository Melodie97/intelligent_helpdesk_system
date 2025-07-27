from langgraph.graph import StateGraph, END
from ..core.state import HelpDeskState
from ..agents.classifier_agent import ClassifierAgent
from ..agents.knowledge_agent import KnowledgeAgent
from ..agents.escalation_agent import EscalationAgent
from ..agents.response_agent import ResponseAgent

class HelpDeskWorkflow:
    def __init__(self):
        self.classifier_agent = ClassifierAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.escalation_agent = EscalationAgent()
        self.response_agent = ResponseAgent()
        
        self.workflow = self._build_workflow()
    
    def _build_workflow(self):
        # Create the state graph
        workflow = StateGraph(HelpDeskState)
        
        # Add nodes (agents)
        workflow.add_node("classify", self.classifier_agent.classify)
        workflow.add_node("retrieve_knowledge", self.knowledge_agent.retrieve_knowledge)
        workflow.add_node("check_escalation", self.escalation_agent.check_escalation)
        workflow.add_node("generate_response", self.response_agent.generate_response)
        
        # Define the workflow edges
        workflow.set_entry_point("classify")
        
        workflow.add_edge("classify", "retrieve_knowledge")
        workflow.add_edge("retrieve_knowledge", "check_escalation")
        workflow.add_edge("check_escalation", "generate_response")
        workflow.add_edge("generate_response", END)
        
        return workflow.compile()
    
    def process_request(self, request: str, user_id: str = None) -> dict:
        initial_state = HelpDeskState(
            request=request,
            user_id=user_id,
            classification=None,
            knowledge_items=[],
            escalate=False,
            escalation_reason=None,
            response="",
            next_action="classify"
        )
        
        # Run the workflow
        result = self.workflow.invoke(initial_state)
        
        return {
            "classification": result["classification"],
            "response": result["response"],
            "knowledge_items": result["knowledge_items"],
            "escalate": result["escalate"],
            "escalation_reason": result["escalation_reason"]
        }