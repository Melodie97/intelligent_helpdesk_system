from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from ..core.state import HelpDeskState

class ResponseAgent:
    def __init__(self):
        llm_provider = os.getenv('LLM_PROVIDER', 'gemini')
        
        if llm_provider == 'gemini':
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-pro",
                google_api_key=os.getenv('GEMINI_API_KEY'),
                temperature=0.7
            )
        else:
            self.llm = ChatOpenAI(
                openai_api_key=os.getenv('OPENAI_API_KEY'),
                temperature=0.7,
                max_tokens=300
            )
        
        self.prompt_template = PromptTemplate(
            input_variables=["request", "category", "context"],
            template="""You are a helpful IT support assistant. A user has submitted the following request:

REQUEST: {request}
CATEGORY: {category}

RELEVANT KNOWLEDGE BASE INFORMATION:
{context}

Please provide a helpful, concise response that:
1. Directly addresses the user's request
2. Uses the relevant knowledge base information
3. Provides clear, actionable steps when possible
4. Maintains a professional but friendly tone
5. Keeps the response under 200 words

RESPONSE:"""
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    def generate_response(self, state: HelpDeskState) -> HelpDeskState:
        if state["escalate"]:
            escalation_reason = state["escalation_reason"] or ""
            state["response"] = f"This request has been escalated to our support team. {escalation_reason} You will receive a response within the next business hour."
        else:
            # Create context from knowledge items
            context = "\n\n".join([
                f"Source: {item.source}\nContent: {item.content}"
                for item in state["knowledge_items"]
            ])
            
            try:
                response = self.chain.run(
                    request=state["request"],
                    category=state["classification"].category.value,
                    context=context
                )
                state["response"] = response.strip()
            except Exception as e:
                state["response"] = "I apologize, but I'm having trouble generating a response right now. Please contact IT support directly."
        
        state["next_action"] = "END"
        return state