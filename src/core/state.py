from typing import TypedDict, List, Optional
from pydantic import BaseModel
from enum import Enum

class RequestCategory(str, Enum):
    PASSWORD_RESET = "password_reset"
    SOFTWARE_INSTALLATION = "software_installation"
    HARDWARE_FAILURE = "hardware_failure"
    NETWORK_CONNECTIVITY = "network_connectivity"
    EMAIL_CONFIGURATION = "email_configuration"
    SECURITY_INCIDENT = "security_incident"
    POLICY_QUESTION = "policy_question"

class KnowledgeItem(BaseModel):
    content: str
    source: str
    relevance_score: float

class ClassificationResult(BaseModel):
    category: RequestCategory
    confidence: float

# API Models
class HelpDeskRequest(BaseModel):
    request: str
    user_id: Optional[str] = None

class HelpDeskResponse(BaseModel):
    request: str
    user_id: Optional[str]
    classification: RequestCategory
    response: str
    escalate: bool
    escalation_reason: Optional[str] = None

# LangGraph State
class HelpDeskState(TypedDict):
    request: str
    user_id: Optional[str]
    classification: Optional[ClassificationResult]
    knowledge_items: List[KnowledgeItem]
    escalate: bool
    escalation_reason: Optional[str]
    response: str
    next_action: str