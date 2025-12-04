"""
Unit tests for RAG Assistant
"""

import pytest
from co_creation_tools.rag import RAGAssistant


class TestRAGAssistant:
    """Test suite for RAG Assistant"""
    
    @pytest.fixture
    def assistant(self):
        """Create RAG Assistant instance"""
        return RAGAssistant()
    
    @pytest.fixture
    def sample_documents(self):
        """Sample documents for testing"""
        return [
            {
                'content': 'Artificial intelligence is transforming industries.',
                'metadata': {'title': 'AI Overview', 'source': 'Test'}
            },
            {
                'content': 'Machine learning models require large datasets.',
                'metadata': {'title': 'ML Basics', 'source': 'Test'}
            }
        ]
    
    def test_initialization(self, assistant):
        """Test RAG Assistant initialization"""
        assert assistant is not None
        assert assistant.knowledge_base == []
        assert assistant.conversation_history == []
    
    def test_add_documents(self, assistant, sample_documents):
        """Test adding documents to knowledge base"""
        assistant.add_documents(sample_documents)
        assert len(assistant.knowledge_base) == 2
        assert assistant.knowledge_base[0].content == sample_documents[0]['content']
    
    def test_query(self, assistant, sample_documents):
        """Test querying the knowledge base"""
        assistant.add_documents(sample_documents)
        result = assistant.query("What is AI?")
        
        assert result is not None
        assert result.query == "What is AI?"
        assert result.generated_response != ""
        assert len(result.relevant_documents) > 0
        assert result.confidence_score > 0
    
    def test_semantic_search(self, assistant, sample_documents):
        """Test semantic search functionality"""
        assistant.add_documents(sample_documents)
        results = assistant._semantic_search("machine learning", top_k=1)
        
        assert len(results) == 1
        assert "machine learning" in results[0].content.lower()
    
    def test_refine_response(self, assistant, sample_documents):
        """Test response refinement"""
        assistant.add_documents(sample_documents)
        original = assistant.query("Explain AI")
        refined = assistant.refine_response("Explain AI", "Make it simpler")
        
        assert refined is not None
        assert refined.query != original.query
    
    def test_co_create_document(self, assistant, sample_documents):
        """Test document co-creation"""
        assistant.add_documents(sample_documents)
        outline = ["Introduction", "Main Content", "Conclusion"]
        document = assistant.co_create_document(outline)
        
        assert document is not None
        assert "Introduction" in document
        assert "Main Content" in document
        assert "Conclusion" in document
    
    def test_get_statistics(self, assistant, sample_documents):
        """Test statistics retrieval"""
        assistant.add_documents(sample_documents)
        assistant.query("Test query")
        
        stats = assistant.get_statistics()
        assert stats['total_documents'] == 2
        assert stats['total_queries'] == 1
        assert 'average_confidence' in stats
