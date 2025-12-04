"""
RAG-Powered AI Assistant for Document Co-Creation

This module implements a Retrieval-Augmented Generation (RAG) system that enables
intelligent document creation, research assistance, and knowledge synthesis.

Use Cases:
- Research paper co-authoring
- Technical documentation generation
- Legal document analysis and drafting
- Business report creation with data integration
"""

import os
from typing import List, Dict, Optional, Tuple
import json
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Document:
    """Represents a document in the knowledge base"""
    id: str
    content: str
    metadata: Dict
    embedding: Optional[List[float]] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


@dataclass
class QueryResult:
    """Represents a query result from the RAG system"""
    query: str
    relevant_documents: List[Document]
    generated_response: str
    confidence_score: float
    sources: List[str]


class RAGAssistant:
    """
    RAG-based AI assistant for intelligent document co-creation.
    
    Features:
    - Semantic search over document collections
    - Context-aware response generation
    - Multi-document synthesis
    - Source attribution and citation
    - Iterative refinement support
    
    Example:
        >>> assistant = RAGAssistant()
        >>> assistant.add_documents([doc1, doc2, doc3])
        >>> result = assistant.query("Summarize the key findings on AI safety")
        >>> print(result.generated_response)
    """
    
    def __init__(self, model_name: str = "gpt2", embedding_model: str = "sentence-transformers"):
        """
        Initialize the RAG Assistant.
        
        Args:
            model_name: Name of the language model to use
            embedding_model: Name of the embedding model for semantic search
        """
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.knowledge_base: List[Document] = []
        self.conversation_history: List[Dict] = []
        
        print(f"[RAG Assistant] Initialized with model: {model_name}")
        
    def add_documents(self, documents: List[Dict]) -> None:
        """
        Add documents to the knowledge base.
        
        Args:
            documents: List of document dictionaries with 'content' and 'metadata'
        """
        for i, doc_dict in enumerate(documents):
            doc = Document(
                id=f"doc_{len(self.knowledge_base) + i}",
                content=doc_dict.get('content', ''),
                metadata=doc_dict.get('metadata', {}),
                embedding=self._compute_embedding(doc_dict.get('content', ''))
            )
            self.knowledge_base.append(doc)
        
        print(f"[RAG Assistant] Added {len(documents)} documents. Total: {len(self.knowledge_base)}")
    
    def _compute_embedding(self, text: str) -> List[float]:
        """
        Compute embedding vector for text (simplified implementation).
        
        In production, this would use actual embedding models like:
        - sentence-transformers
        - OpenAI embeddings
        - Cohere embeddings
        """
        # Simplified: Hash-based pseudo-embedding for demonstration
        # In real implementation, use proper embedding models
        hash_val = hash(text)
        return [float((hash_val >> i) & 0xFF) / 255.0 for i in range(0, 384, 8)]
    
    def _semantic_search(self, query: str, top_k: int = 5) -> List[Document]:
        """
        Perform semantic search over the knowledge base.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of most relevant documents
        """
        query_embedding = self._compute_embedding(query)
        
        # Simplified similarity calculation
        # In production, use cosine similarity with proper embeddings
        scored_docs = []
        for doc in self.knowledge_base:
            # Simple keyword matching for demonstration
            query_words = set(query.lower().split())
            doc_words = set(doc.content.lower().split())
            similarity = len(query_words & doc_words) / max(len(query_words), 1)
            scored_docs.append((similarity, doc))
        
        # Sort by similarity and return top k
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        return [doc for _, doc in scored_docs[:top_k]]
    
    def _generate_response(self, query: str, context_docs: List[Document]) -> Tuple[str, float]:
        """
        Generate response based on query and retrieved documents.
        
        Args:
            query: User query
            context_docs: Retrieved context documents
            
        Returns:
            Tuple of (generated_response, confidence_score)
        """
        # Build context from retrieved documents
        context = "\n\n".join([
            f"[Source {i+1}]: {doc.content[:500]}"
            for i, doc in enumerate(context_docs)
        ])
        
        # In production, this would call an actual LLM API
        # For demonstration, we create a structured response
        response = f"""Based on the retrieved information:

Query: {query}

Key Findings:
{self._extract_key_points(context_docs)}

Synthesis:
The documents provide insights on {query.lower()}. {self._summarize_context(context_docs)}

This response is synthesized from {len(context_docs)} relevant sources in the knowledge base."""
        
        # Calculate confidence based on document relevance
        confidence = min(0.95, 0.5 + (len(context_docs) * 0.1))
        
        return response, confidence
    
    def _extract_key_points(self, docs: List[Document], max_points: int = 3) -> str:
        """Extract key points from documents"""
        points = []
        for i, doc in enumerate(docs[:max_points]):
            # Extract first sentence or up to 100 chars
            content = doc.content.split('.')[0] if '.' in doc.content else doc.content[:100]
            points.append(f"• {content}")
        return "\n".join(points)
    
    def _summarize_context(self, docs: List[Document]) -> str:
        """Create a brief summary of the context"""
        total_words = sum(len(doc.content.split()) for doc in docs)
        topics = set()
        for doc in docs:
            topics.update(word for word in doc.content.lower().split() if len(word) > 5)
        
        return f"Analysis covers approximately {total_words} words across {len(docs)} documents, focusing on topics including {', '.join(list(topics)[:5])}."
    
    def query(self, question: str, top_k: int = 5) -> QueryResult:
        """
        Query the RAG system with a question.
        
        Args:
            question: User's question or prompt
            top_k: Number of documents to retrieve
            
        Returns:
            QueryResult with generated response and sources
        """
        # Retrieve relevant documents
        relevant_docs = self._semantic_search(question, top_k)
        
        # Generate response
        response, confidence = self._generate_response(question, relevant_docs)
        
        # Extract sources
        sources = [
            f"{doc.metadata.get('title', doc.id)}: {doc.metadata.get('source', 'Internal')}"
            for doc in relevant_docs
        ]
        
        # Create result
        result = QueryResult(
            query=question,
            relevant_documents=relevant_docs,
            generated_response=response,
            confidence_score=confidence,
            sources=sources
        )
        
        # Add to conversation history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'query': question,
            'response': response,
            'confidence': confidence
        })
        
        return result
    
    def refine_response(self, original_query: str, feedback: str) -> QueryResult:
        """
        Refine a previous response based on user feedback.
        
        Args:
            original_query: The original query
            feedback: User's feedback or refinement request
            
        Returns:
            Refined QueryResult
        """
        # Combine original query with feedback
        refined_query = f"{original_query} [REFINEMENT: {feedback}]"
        
        print(f"[RAG Assistant] Refining response based on feedback: {feedback}")
        
        # Re-query with refinement context
        return self.query(refined_query)
    
    def co_create_document(self, outline: List[str], sources: Optional[List[str]] = None) -> str:
        """
        Co-create a document based on an outline.
        
        Args:
            outline: List of section headings/topics
            sources: Optional list of specific sources to use
            
        Returns:
            Generated document content
        """
        print(f"[RAG Assistant] Co-creating document with {len(outline)} sections")
        
        document_sections = []
        
        for i, section in enumerate(outline):
            print(f"  Generating section {i+1}/{len(outline)}: {section}")
            
            # Query for each section
            result = self.query(f"Write about: {section}")
            
            section_content = f"""## {section}

{result.generated_response}

*Sources: {', '.join(result.sources[:3])}*
"""
            document_sections.append(section_content)
        
        # Combine sections
        full_document = f"""# Co-Created Document
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Generated by: RAG Assistant*

---

{''.join(document_sections)}

---

## References
{self._generate_references()}
"""
        
        return full_document
    
    def _generate_references(self) -> str:
        """Generate a references section from knowledge base"""
        references = []
        for i, doc in enumerate(self.knowledge_base[:10], 1):
            title = doc.metadata.get('title', f'Document {doc.id}')
            source = doc.metadata.get('source', 'Internal')
            references.append(f"{i}. {title} - {source}")
        
        return "\n".join(references)
    
    def export_conversation(self, filepath: str) -> None:
        """Export conversation history to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
        print(f"[RAG Assistant] Conversation exported to {filepath}")
    
    def get_statistics(self) -> Dict:
        """Get statistics about the RAG system"""
        return {
            'total_documents': len(self.knowledge_base),
            'total_queries': len(self.conversation_history),
            'average_confidence': sum(q['confidence'] for q in self.conversation_history) / max(len(self.conversation_history), 1),
            'knowledge_base_size_kb': sum(len(doc.content) for doc in self.knowledge_base) / 1024
        }


# Example usage and real-world scenario
if __name__ == "__main__":
    # Initialize RAG Assistant
    assistant = RAGAssistant(model_name="gpt-3.5-turbo")
    
    # Add sample research documents
    sample_docs = [
        {
            'content': 'Recent advances in large language models have revolutionized natural language processing. Models like GPT-4 and Claude demonstrate unprecedented capabilities in understanding and generating human-like text.',
            'metadata': {'title': 'LLM Survey 2024', 'source': 'AI Research Journal'}
        },
        {
            'content': 'Retrieval-Augmented Generation (RAG) combines the benefits of retrieval-based and generation-based approaches. By retrieving relevant information before generation, RAG systems produce more accurate and grounded responses.',
            'metadata': {'title': 'RAG Architecture Guide', 'source': 'ML Conference Proceedings'}
        },
        {
            'content': 'AI safety and alignment remain critical challenges. Ensuring AI systems behave according to human values and intentions requires ongoing research in reward modeling, constitutional AI, and interpretability.',
            'metadata': {'title': 'AI Safety Handbook', 'source': 'Ethics in AI Institute'}
        }
    ]
    
    assistant.add_documents(sample_docs)
    
    # Query the system
    result = assistant.query("What are the key developments in language models?")
    print("\n" + "="*80)
    print("QUERY RESULT:")
    print("="*80)
    print(f"Query: {result.query}")
    print(f"Confidence: {result.confidence_score:.2%}")
    print(f"\nResponse:\n{result.generated_response}")
    print(f"\nSources: {', '.join(result.sources)}")
    
    # Co-create a document
    print("\n" + "="*80)
    print("CO-CREATING DOCUMENT:")
    print("="*80)
    outline = [
        "Introduction to Modern AI",
        "Retrieval-Augmented Generation",
        "Future Directions"
    ]
    document = assistant.co_create_document(outline)
    print(document)
    
    # Get statistics
    stats = assistant.get_statistics()
    print("\n" + "="*80)
    print("SYSTEM STATISTICS:")
    print("="*80)
    for key, value in stats.items():
        print(f"{key}: {value}")
