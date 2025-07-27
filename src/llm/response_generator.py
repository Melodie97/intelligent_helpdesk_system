from langchain.llms import OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import List
from src.core.models import KnowledgeItem, RequestCategory
from config.settings import Config

class ResponseGenerator:
    def __init__(self):
        self.config = Config()
        if not self.config.validate():
            raise ValueError("Invalid configuration for LLM provider")
        
        # Initialize LLM based on provider
        if self.config.llm_provider == 'gemini':
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=self.config.gemini_api_key,
                temperature=0.7
            )
        elif self.config.llm_provider == 'openai':
            self.llm = OpenAI(
                openai_api_key=self.config.openai_api_key,
                temperature=0.7,
                max_tokens=300
            )
        
        # Create prompt template
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
        
        # Create LLM chain
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    def generate_response(self, request: str, category: RequestCategory, 
                         knowledge_items: List[KnowledgeItem]) -> str:
        # Create context from knowledge items
        context = "\n\n".join([
            f"Source: {item.source}\nContent: {item.content}"
            for item in knowledge_items
        ])
        
        try:
            # Use LangChain chain to generate response
            response = self.chain.run(
                request=request,
                category=category.value,
                context=context
            )
            return response.strip()
        except Exception as e:
            # Fallback response if LLM fails
            return self._generate_fallback_response(category, knowledge_items)
    
    def _generate_fallback_response(self, category: RequestCategory, 
                                  knowledge_items: List[KnowledgeItem]) -> str:
        if not knowledge_items:
            return f"I understand you have a {category.value.replace('_', ' ')} issue. Please contact IT support for assistance."
        
        # Use first knowledge item as basis for response
        first_item = knowledge_items[0]
        return f"Based on our knowledge base, here's what I found: {first_item.content[:200]}... For more detailed assistance, please contact IT support."