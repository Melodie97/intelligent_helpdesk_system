from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class RequestCategory(str, Enum):
    PASSWORD_RESET = "password_reset"
    SOFTWARE_INSTALLATION = "software_installation"
    HARDWARE_FAILURE = "hardware_failure"
    NETWORK_CONNECTIVITY = "network_connectivity"
    EMAIL_CONFIGURATION = "email_configuration"
    SECURITY_INCIDENT = "security_incident"
    POLICY_QUESTION = "policy_question"

class HelpDeskRequest(BaseModel):
    request: str
    user_id: Optional[str] = None

class ClassificationResult(BaseModel):
    category: RequestCategory
    confidence: float

class KnowledgeItem(BaseModel):
    content: str
    source: str
    relevance_score: float

class HelpDeskResponse(BaseModel):
    classification: ClassificationResult
    response: str
    knowledge_items: List[KnowledgeItem]
    escalate: bool
    escalation_reason: Optional[str] = None