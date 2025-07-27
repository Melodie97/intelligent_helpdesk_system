from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import json
import os
from ..core.state import HelpDeskState, KnowledgeItem

class KnowledgeAgent:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        self.vectorstore = self._build_vectorstore()
    
    def _build_vectorstore(self):
        documents = []
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        
        # Load knowledge base
        kb_file = os.path.join(data_dir, 'knowledge_base.md')
        with open(kb_file, 'r') as f:
            content = f.read()
            sections = content.split('## ')
            for section in sections[1:]:
                title = section.split('\n')[0]
                body = '\n'.join(section.split('\n')[1:])
                doc = Document(
                    page_content=body.strip(),
                    metadata={'source': f'knowledge_base.md#{title}'}
                )
                documents.append(doc)
        
        # Load troubleshooting database
        ts_file = os.path.join(data_dir, 'troubleshooting_database.json')
        with open(ts_file, 'r') as f:
            troubleshooting = json.load(f)
            for key, item in troubleshooting['troubleshooting_steps'].items():
                content = f"Steps: {' '.join(item['steps'])}"
                doc = Document(
                    page_content=content,
                    metadata={'source': f'troubleshooting_database.json#{key}'}
                )
                documents.append(doc)
        
        return FAISS.from_documents(documents, self.embeddings)
    
    def retrieve_knowledge(self, state: HelpDeskState) -> HelpDeskState:
        request = state["request"]
        
        # Get similar documents
        docs = self.vectorstore.similarity_search_with_score(request, k=6)
        
        # Sort by score and take top 3
        docs.sort(key=lambda x: x[1])
        
        knowledge_items = []
        for doc, score in docs[:3]:
            knowledge_items.append(KnowledgeItem(
                content=doc.page_content,
                source=doc.metadata['source'],
                relevance_score=float(1.0 - score)
            ))
        
        state["knowledge_items"] = knowledge_items
        state["next_action"] = "check_escalation"
        
        return state