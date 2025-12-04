"""
RAG Assistant Demo: Research Paper Co-Authoring

This example demonstrates how to use the RAG Assistant for research paper co-authoring,
including document ingestion, querying, and structured document generation.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from co_creation_tools.rag import RAGAssistant


def main():
    """Run RAG Assistant demo"""
    
    print("="*80)
    print("RAG ASSISTANT DEMO: Research Paper Co-Authoring")
    print("="*80)
    
    # Initialize assistant
    print("\n📚 Initializing RAG Assistant...")
    assistant = RAGAssistant(model_name="research-llm")
    
    # Sample research documents
    research_papers = [
        {
            'content': '''
Large Language Models (LLMs) have revolutionized natural language processing 
through their unprecedented scale and capabilities. Recent models like GPT-4, 
Claude, and PaLM demonstrate emergent abilities in reasoning, code generation, 
and multi-task learning. These models are trained on trillions of tokens and 
contain hundreds of billions of parameters, enabling them to perform complex 
tasks with minimal fine-tuning.
            ''',
            'metadata': {
                'title': 'Scaling Language Models: Emergent Abilities',
                'authors': 'Wei et al.',
                'year': 2024,
                'source': 'AI Research Journal'
            }
        },
        {
            'content': '''
Retrieval-Augmented Generation (RAG) combines the benefits of parametric and 
non-parametric approaches to language modeling. By retrieving relevant 
information from external knowledge bases before generation, RAG systems 
produce more accurate, factual, and grounded responses. This approach 
significantly reduces hallucination rates and improves performance on 
knowledge-intensive tasks.
            ''',
            'metadata': {
                'title': 'RAG: Retrieval-Augmented Generation for Knowledge-Intensive NLP',
                'authors': 'Lewis et al.',
                'year': 2023,
                'source': 'NeurIPS 2023'
            }
        },
        {
            'content': '''
AI safety and alignment remain critical challenges as models become more 
capable. Key research areas include reward modeling, constitutional AI, 
red teaming, and interpretability. Ensuring AI systems behave according to 
human values requires multi-faceted approaches including technical solutions, 
governance frameworks, and ongoing monitoring.
            ''',
            'metadata': {
                'title': 'AI Safety: Challenges and Solutions',
                'authors': 'Anthropic Research Team',
                'year': 2024,
                'source': 'AI Safety Journal'
            }
        },
        {
            'content': '''
Few-shot and zero-shot learning capabilities of LLMs enable rapid adaptation 
to new tasks without extensive fine-tuning. Through careful prompt engineering 
and in-context learning, models can perform tasks they were never explicitly 
trained on. This flexibility makes LLMs powerful tools for diverse applications 
from creative writing to scientific analysis.
            ''',
            'metadata': {
                'title': 'In-Context Learning and Few-Shot Capabilities',
                'authors': 'Brown et al.',
                'year': 2023,
                'source': 'Machine Learning Conference'
            }
        }
    ]
    
    # Add documents to knowledge base
    print(f"\n📥 Adding {len(research_papers)} research papers to knowledge base...")
    assistant.add_documents(research_papers)
    
    # Display statistics
    stats = assistant.get_statistics()
    print(f"\n📊 Knowledge Base Statistics:")
    print(f"   • Total Documents: {stats['total_documents']}")
    print(f"   • Size: {stats['knowledge_base_size_kb']:.2f} KB")
    
    # Example 1: Query the knowledge base
    print("\n" + "="*80)
    print("EXAMPLE 1: Querying the Knowledge Base")
    print("="*80)
    
    query = "What are the key developments in large language models?"
    print(f"\n❓ Query: {query}")
    
    result = assistant.query(query, top_k=3)
    
    print(f"\n📊 Confidence: {result.confidence_score:.1%}")
    print(f"📚 Sources Used: {len(result.sources)}")
    
    print(f"\n💬 Response:")
    print(result.generated_response)
    
    print(f"\n📖 Sources:")
    for i, source in enumerate(result.sources, 1):
        print(f"   {i}. {source}")
    
    # Example 2: Iterative refinement
    print("\n" + "="*80)
    print("EXAMPLE 2: Iterative Refinement")
    print("="*80)
    
    feedback = "Focus more on practical applications and real-world impact"
    print(f"\n💭 Feedback: {feedback}")
    
    refined = assistant.refine_response(query, feedback)
    print(f"\n✨ Refined Response:")
    print(refined.generated_response)
    
    # Example 3: Co-create a research paper section
    print("\n" + "="*80)
    print("EXAMPLE 3: Co-Creating Research Paper")
    print("="*80)
    
    outline = [
        "Introduction: The Rise of Large Language Models",
        "Retrieval-Augmented Generation",
        "Safety and Alignment Considerations",
        "Future Directions and Conclusions"
    ]
    
    print(f"\n📝 Generating paper with {len(outline)} sections...")
    document = assistant.co_create_document(outline)
    
    print("\n📄 Generated Research Paper:")
    print(document[:1000] + "...\n[truncated for display]")
    
    # Save document
    output_file = "generated_research_paper.md"
    with open(output_file, 'w') as f:
        f.write(document)
    print(f"\n💾 Full document saved to: {output_file}")
    
    # Example 4: Export conversation history
    print("\n" + "="*80)
    print("EXAMPLE 4: Export Conversation History")
    print("="*80)
    
    conversation_file = "conversation_history.json"
    assistant.export_conversation(conversation_file)
    
    print(f"\n📊 Final Statistics:")
    final_stats = assistant.get_statistics()
    for key, value in final_stats.items():
        print(f"   • {key}: {value}")
    
    print("\n" + "="*80)
    print("✅ Demo completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()
