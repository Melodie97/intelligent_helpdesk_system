from langchain.document_loaders import TextLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from typing import List
import json
from .models import KnowledgeItem, RequestCategory
from config.settings import Config

class KnowledgeRetriever:
    def __init__(self):
        self.config = Config()
        self.embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        self.vectorstore = self._build_vectorstore()
    
    def _build_vectorstore(self):
        documents = []
        
        # Load main knowledge base
        with open(self.config.knowledge_base_file, 'r') as f:
            content = f.read()
            sections = content.split('## ')
            for section in sections[1:]:  # Skip first empty section
                title = section.split('\n')[0]
                body = '\n'.join(section.split('\n')[1:])
                doc = Document(
                    page_content=body.strip(),
                    metadata={
                        'source': f'knowledge_base.md#{title}',
                        'category': self._infer_category(title)
                    }
                )
                documents.append(doc)
        
        # Load troubleshooting database
        with open(self.config.troubleshooting_file, 'r') as f:
            troubleshooting = json.load(f)
            for key, item in troubleshooting['troubleshooting_steps'].items():
                content = f"Steps: {' '.join(item['steps'])}"
                doc = Document(
                    page_content=content,
                    metadata={
                        'source': f'troubleshooting_database.json#{key}',
                        'category': self._infer_category(key)
                    }
                )
                documents.append(doc)
        
        # Load installation guides
        with open(self.config.installation_guides_file, 'r') as f:
            guides = json.load(f)
            for software, guide in guides['software_guides'].items():
                content = f"{guide['title']}: {' '.join(guide['steps'])}"
                doc = Document(
                    page_content=content,
                    metadata={
                        'source': f'installation_guides.json#{software}',
                        'category': 'software_installation'
                    }
                )
                documents.append(doc)
        
        # Load company policies
        with open(self.config.policies_file, 'r') as f:
            content = f.read()
            sections = content.split('## ')
            for section in sections[1:]:
                title = section.split('\n')[0]
                body = '\n'.join(section.split('\n')[1:])
                doc = Document(
                    page_content=body.strip(),
                    metadata={
                        'source': f'company_it_policies.md#{title}',
                        'category': 'policy_question'
                    }
                )
                documents.append(doc)
        
        return FAISS.from_documents(documents, self.embeddings)
    
    def _infer_category(self, title: str) -> str:
        title_lower = title.lower()
        if 'password' in title_lower:
            return 'password_reset'
        elif 'network' in title_lower or 'wifi' in title_lower:
            return 'network_connectivity'
        elif 'email' in title_lower:
            return 'email_configuration'
        elif 'software' in title_lower or 'installation' in title_lower:
            return 'software_installation'
        elif 'hardware' in title_lower:
            return 'hardware_failure'
        elif 'security' in title_lower:
            return 'security_incident'
        else:
            return 'policy_question'
    
    def retrieve(self, query: str, category: RequestCategory, top_k: int = 3) -> List[KnowledgeItem]:
        # Get similar documents
        docs = self.vectorstore.similarity_search_with_score(query, k=top_k*2)
        
        # Prioritize category-matching documents
        scored_docs = []
        for doc, score in docs:
            # Boost score for category-matching documents
            if doc.metadata.get('category') == category.value:
                score *= 0.7  # Lower score is better in FAISS
            scored_docs.append((doc, score))
        
        # Sort by score and take top_k
        scored_docs.sort(key=lambda x: x[1])
        
        results = []
        for doc, score in scored_docs[:top_k]:
            results.append(KnowledgeItem(
                content=doc.page_content,
                source=doc.metadata['source'],
                relevance_score=float(1.0 - score)  # Convert to similarity score
            ))
        
        return results