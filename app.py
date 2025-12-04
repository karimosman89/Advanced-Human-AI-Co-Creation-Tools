"""
Advanced Human-AI Co-Creation Tools - Interactive Demo

A comprehensive Streamlit application demonstrating all co-creation capabilities.

Run with: streamlit run app.py
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from co_creation_tools.rag import RAGAssistant
from co_creation_tools.creative_studio import MultimodalCreator
from co_creation_tools.code_assistant import CodeReviewer

# Page configuration
st.set_page_config(
    page_title="Advanced Human-AI Co-Creation Tools",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .feature-box {
        border: 2px solid #667eea;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Advanced Human-AI Co-Creation Tools</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform your workflow with intelligent AI assistance</p>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.radio(
        "Select Tool",
        ["🏠 Home", "📚 RAG Assistant", "🎨 Creative Studio", "💻 Code Reviewer"]
    )
    
    # Initialize session state
    if 'rag_assistant' not in st.session_state:
        st.session_state.rag_assistant = None
    if 'creator' not in st.session_state:
        st.session_state.creator = None
    if 'reviewer' not in st.session_state:
        st.session_state.reviewer = None
    
    # Route to pages
    if page == "🏠 Home":
        show_home_page()
    elif page == "📚 RAG Assistant":
        show_rag_page()
    elif page == "🎨 Creative Studio":
        show_creative_page()
    elif page == "💻 Code Reviewer":
        show_code_reviewer_page()


def show_home_page():
    """Show home page with overview"""
    
    st.markdown("---")
    
    # Introduction
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>📚 RAG Assistant</h3>
            <p>Intelligent document co-creation with retrieval-augmented generation</p>
            <ul>
                <li>Research synthesis</li>
                <li>Document generation</li>
                <li>Knowledge base queries</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>🎨 Creative Studio</h3>
            <p>Multimodal content creation across text, images, and code</p>
            <ul>
                <li>Marketing campaigns</li>
                <li>Technical content</li>
                <li>Creative variations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h3>💻 Code Reviewer</h3>
            <p>AI-powered code analysis and improvement suggestions</p>
            <ul>
                <li>Security scanning</li>
                <li>Performance analysis</li>
                <li>Test generation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Real-world use cases
    st.header("🌟 Real-World Use Cases")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Research & Academia", "Marketing & Business", "Software Development", "Creative Industries"])
    
    with tab1:
        st.subheader("Research & Academia")
        st.write("""
        **Use Case**: Literature Review & Paper Co-Authoring
        - Analyze 100+ research papers automatically
        - Extract key findings and synthesize insights
        - Generate literature review sections
        - Maintain proper citations and references
        
        **Impact**: Reduce research time by 60%, maintain academic rigor
        """)
        
        st.code("""
# Example: Research Paper Co-Creation
assistant = RAGAssistant()
assistant.add_documents(research_papers)
document = assistant.co_create_document([
    "Introduction to AI Safety",
    "Current Challenges",
    "Proposed Solutions",
    "Conclusion"
])
        """, language="python")
    
    with tab2:
        st.subheader("Marketing & Business")
        st.write("""
        **Use Case**: Multi-Channel Marketing Campaign Generation
        - Create consistent brand messaging across channels
        - Generate social media, email, and web content
        - Produce visual concepts and copy variations
        - Maintain brand voice and guidelines
        
        **Impact**: Launch campaigns 10x faster, maintain quality
        """)
        
        st.code("""
# Example: Campaign Creation
creator = MultimodalCreator()
campaign = creator.create_marketing_campaign(
    product_name="AI Tools Suite",
    target_audience="Tech professionals",
    key_message="Transform your workflow",
    channels=['social', 'email', 'web']
)
        """, language="python")
    
    with tab3:
        st.subheader("Software Development")
        st.write("""
        **Use Case**: Automated Code Review & Security Analysis
        - Detect security vulnerabilities automatically
        - Enforce coding standards and best practices
        - Generate unit tests and documentation
        - Suggest performance optimizations
        
        **Impact**: Catch 90% of issues before human review
        """)
        
        st.code("""
# Example: Code Review
reviewer = CodeReviewer(strict_mode=True)
result = reviewer.review_code(source_code, "app.py")
tests = reviewer.generate_tests(source_code)
refactoring = reviewer.suggest_refactoring(source_code)
        """, language="python")
    
    with tab4:
        st.subheader("Creative Industries")
        st.write("""
        **Use Case**: Multi-Style Content Generation
        - Create content variations for A/B testing
        - Generate educational materials in different formats
        - Produce creative variations for design exploration
        - Maintain consistency across deliverables
        
        **Impact**: Explore 20+ variations in minutes
        """)
    
    st.markdown("---")
    
    # Statistics
    st.header("📊 Platform Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tools Available", "3", delta="Production Ready")
    with col2:
        st.metric("Use Cases", "15+", delta="Across Industries")
    with col3:
        st.metric("Time Saved", "10x", delta="Average Improvement")
    with col4:
        st.metric("Quality Score", "A+", delta="Consistent Output")


def show_rag_page():
    """RAG Assistant page"""
    
    st.header("📚 RAG-Powered Document Co-Creation")
    st.write("Create intelligent documents with retrieval-augmented generation")
    
    # Initialize RAG if needed
    if st.session_state.rag_assistant is None:
        with st.spinner("Initializing RAG Assistant..."):
            st.session_state.rag_assistant = RAGAssistant()
        st.success("✅ RAG Assistant initialized!")
    
    assistant = st.session_state.rag_assistant
    
    # Tabs for different features
    tab1, tab2, tab3 = st.tabs(["📄 Add Documents", "❓ Query", "📝 Co-Create Document"])
    
    with tab1:
        st.subheader("Add Documents to Knowledge Base")
        
        num_docs = st.number_input("Number of documents to add", min_value=1, max_value=10, value=1)
        
        docs_to_add = []
        for i in range(num_docs):
            with st.expander(f"Document {i+1}"):
                title = st.text_input(f"Title {i+1}", key=f"doc_title_{i}")
                source = st.text_input(f"Source {i+1}", key=f"doc_source_{i}")
                content = st.text_area(f"Content {i+1}", height=150, key=f"doc_content_{i}")
                
                if title and content:
                    docs_to_add.append({
                        'content': content,
                        'metadata': {'title': title, 'source': source}
                    })
        
        if st.button("Add Documents to Knowledge Base"):
            if docs_to_add:
                assistant.add_documents(docs_to_add)
                st.success(f"✅ Added {len(docs_to_add)} documents!")
                
                stats = assistant.get_statistics()
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Documents", stats['total_documents'])
                with col2:
                    st.metric("KB Size", f"{stats['knowledge_base_size_kb']:.2f} KB")
            else:
                st.warning("Please add at least one document with title and content")
    
    with tab2:
        st.subheader("Query the Knowledge Base")
        
        query = st.text_input("Enter your question:")
        top_k = st.slider("Number of documents to retrieve", 1, 10, 5)
        
        if st.button("Submit Query"):
            if query:
                with st.spinner("Searching knowledge base..."):
                    result = assistant.query(query, top_k=top_k)
                
                st.success("✅ Query completed!")
                
                # Display results
                st.markdown("### 📊 Results")
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.metric("Confidence", f"{result.confidence_score:.1%}")
                with col2:
                    st.metric("Sources Used", len(result.sources))
                
                st.markdown("### 💬 Response")
                st.write(result.generated_response)
                
                with st.expander("📚 View Sources"):
                    for i, source in enumerate(result.sources, 1):
                        st.write(f"{i}. {source}")
                
                # Allow refinement
                st.markdown("### ✨ Refine Response")
                feedback = st.text_input("Provide feedback or refinement request:")
                if st.button("Refine"):
                    if feedback:
                        refined = assistant.refine_response(query, feedback)
                        st.write("**Refined Response:**")
                        st.write(refined.generated_response)
            else:
                st.warning("Please enter a query")
    
    with tab3:
        st.subheader("Co-Create a Document")
        
        st.write("Define the outline for your document:")
        
        num_sections = st.number_input("Number of sections", min_value=1, max_value=10, value=3)
        
        outline = []
        for i in range(num_sections):
            section = st.text_input(f"Section {i+1} heading", key=f"section_{i}")
            if section:
                outline.append(section)
        
        if st.button("Generate Document"):
            if outline:
                with st.spinner("Co-creating document..."):
                    document = assistant.co_create_document(outline)
                
                st.success("✅ Document generated!")
                
                st.markdown("### 📄 Generated Document")
                st.markdown(document)
                
                # Download button
                st.download_button(
                    label="📥 Download Document",
                    data=document,
                    file_name="co_created_document.md",
                    mime="text/markdown"
                )
            else:
                st.warning("Please define at least one section")


def show_creative_page():
    """Creative Studio page"""
    
    st.header("🎨 Multimodal Creative Studio")
    st.write("Create compelling content across multiple formats")
    
    # Initialize Creator if needed
    if st.session_state.creator is None:
        with st.spinner("Initializing Creative Studio..."):
            st.session_state.creator = MultimodalCreator()
        st.success("✅ Creative Studio initialized!")
    
    creator = st.session_state.creator
    
    # Tabs for different features
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Text Generation", "🖼️ Image Prompts", "💻 Code Generation", "📢 Marketing Campaign"])
    
    with tab1:
        st.subheader("AI-Powered Text Generation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            prompt = st.text_area("What would you like to create?", height=100)
            style = st.selectbox("Writing Style", [
                "Professional", "Marketing", "Technical", 
                "Creative", "Educational", "Casual"
            ])
        
        with col2:
            max_length = st.slider("Maximum Length (words)", 100, 2000, 500)
            num_variations = st.slider("Number of Variations", 1, 5, 2)
        
        if st.button("Generate Text"):
            if prompt:
                # Create project if doesn't exist
                if not creator.projects:
                    project = creator.create_project("Demo Project", "Interactive demo session")
                else:
                    project = list(creator.projects.values())[0]
                
                with st.spinner("Generating text..."):
                    from co_creation_tools.creative_studio.multimodal_creator import Style
                    style_enum = Style[style.upper().replace(" ", "_")]
                    
                    result = creator.generate_text(
                        project_id=project.project_id,
                        prompt=prompt,
                        style=style_enum,
                        max_length=max_length,
                        num_variations=num_variations
                    )
                
                st.success(f"✅ Generated {num_variations} variation(s)!")
                
                for variation in result['variations']:
                    with st.expander(f"Variation {variation['variation_id']} ({variation['word_count']} words)"):
                        st.write(variation['text'])
                        
                        st.download_button(
                            label=f"📥 Download Variation {variation['variation_id']}",
                            data=variation['text'],
                            file_name=f"variation_{variation['variation_id']}.txt",
                            mime="text/plain",
                            key=f"download_{variation['variation_id']}"
                        )
            else:
                st.warning("Please enter a prompt")
    
    with tab2:
        st.subheader("Image Generation Prompts")
        
        description = st.text_area("Describe the image you want to create:", height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            img_style = st.selectbox("Visual Style", [
                "photorealistic", "artistic", "minimalist", "cinematic", "corporate"
            ])
        with col2:
            aspect_ratio = st.selectbox("Aspect Ratio", ["16:9", "9:16", "1:1", "4:3"])
        
        if st.button("Generate Image Prompt"):
            if description:
                if not creator.projects:
                    project = creator.create_project("Demo Project", "Interactive demo session")
                else:
                    project = list(creator.projects.values())[0]
                
                result = creator.generate_image_prompt(
                    project_id=project.project_id,
                    description=description,
                    style=img_style,
                    aspect_ratio=aspect_ratio
                )
                
                st.success("✅ Image prompt optimized!")
                
                st.markdown("### 🎯 Optimized Prompt")
                st.code(result['optimized_prompt'])
                
                with st.expander("📋 See All Variations"):
                    for i, var in enumerate(result['prompt_variations'], 1):
                        st.write(f"**Variation {i}:**")
                        st.code(var)
                
                with st.expander("⚙️ Generation Parameters"):
                    st.json(result['generation_params'])
            else:
                st.warning("Please enter an image description")
    
    with tab3:
        st.subheader("AI Code Generation")
        
        code_desc = st.text_area("Describe the functionality you need:", height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            language = st.selectbox("Programming Language", ["python", "javascript", "typescript", "java", "go"])
        with col2:
            framework = st.text_input("Framework (optional)", "")
        
        if st.button("Generate Code"):
            if code_desc:
                if not creator.projects:
                    project = creator.create_project("Demo Project", "Interactive demo session")
                else:
                    project = list(creator.projects.values())[0]
                
                with st.spinner("Generating code..."):
                    result = creator.generate_code(
                        project_id=project.project_id,
                        description=code_desc,
                        language=language,
                        framework=framework if framework else None
                    )
                
                st.success(f"✅ Generated {result['lines_of_code']} lines of code!")
                
                st.markdown("### 💻 Generated Code")
                st.code(result['code'], language=language)
                
                with st.expander("📚 Documentation"):
                    st.markdown(result['documentation'])
                
                st.download_button(
                    label="📥 Download Code",
                    data=result['code'],
                    file_name=f"generated_code.{language}",
                    mime="text/plain"
                )
            else:
                st.warning("Please describe the functionality you need")
    
    with tab4:
        st.subheader("Complete Marketing Campaign")
        
        st.write("Generate a comprehensive multi-channel marketing campaign")
        
        product_name = st.text_input("Product/Service Name")
        target_audience = st.text_input("Target Audience")
        key_message = st.text_area("Key Marketing Message", height=80)
        
        channels = st.multiselect(
            "Marketing Channels",
            ["social", "email", "web", "ads", "print"],
            default=["social", "email", "web"]
        )
        
        if st.button("Create Campaign"):
            if product_name and target_audience and key_message:
                with st.spinner("Creating comprehensive marketing campaign..."):
                    campaign = creator.create_marketing_campaign(
                        product_name=product_name,
                        target_audience=target_audience,
                        key_message=key_message,
                        channels=channels
                    )
                
                st.success("✅ Campaign created successfully!")
                
                # Show campaign summary
                summary = creator.get_project_summary(campaign.project_id)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Assets", summary['total_assets'])
                with col2:
                    st.metric("Asset Types", len(summary['asset_breakdown']))
                with col3:
                    st.metric("Channels", len(channels))
                
                # Show assets
                st.markdown("### 📦 Generated Assets")
                
                for asset in campaign.assets:
                    with st.expander(f"{asset['type'].upper()} - {asset['asset_id']}"):
                        if asset['type'] == 'text':
                            st.write(f"**Prompt:** {asset.get('prompt', 'N/A')}")
                            st.write(f"**Style:** {asset.get('style', 'N/A')}")
                            for var in asset.get('variations', []):
                                st.markdown(f"**Variation {var['variation_id']}:**")
                                st.write(var['text'])
                        elif asset['type'] == 'image_prompt':
                            st.write(f"**Description:** {asset.get('description', 'N/A')}")
                            st.code(asset.get('optimized_prompt', 'N/A'))
                
                # Export option
                if st.button("Export Campaign"):
                    export_path = creator.export_project(campaign.project_id, format="markdown")
                    st.success(f"Campaign exported to: {export_path}")
            else:
                st.warning("Please fill in all campaign details")


def show_code_reviewer_page():
    """Code Reviewer page"""
    
    st.header("💻 AI-Powered Code Review")
    st.write("Comprehensive code analysis and improvement suggestions")
    
    # Initialize Reviewer if needed
    if st.session_state.reviewer is None:
        with st.spinner("Initializing Code Reviewer..."):
            st.session_state.reviewer = CodeReviewer(strict_mode=False)
        st.success("✅ Code Reviewer initialized!")
    
    reviewer = st.session_state.reviewer
    
    # Tabs for different features
    tab1, tab2, tab3 = st.tabs(["🔍 Code Review", "✨ Refactoring", "🧪 Test Generation"])
    
    with tab1:
        st.subheader("Comprehensive Code Review")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            code = st.text_area("Paste your code here:", height=300, key="review_code")
        
        with col2:
            filename = st.text_input("Filename", "code.py")
            language = st.selectbox("Language", ["python", "javascript", "java", "go"])
            strict_mode = st.checkbox("Strict Mode", value=False)
        
        if st.button("Review Code"):
            if code:
                reviewer.strict_mode = strict_mode
                
                with st.spinner("Analyzing code..."):
                    result = reviewer.review_code(code, filename, language)
                
                st.success("✅ Review completed!")
                
                # Display metrics
                st.markdown("### 📊 Code Metrics")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Quality Grade", result.metrics.get('grade', 'N/A'))
                with col2:
                    st.metric("Lines of Code", result.metrics['lines_of_code'])
                with col3:
                    st.metric("Complexity", result.metrics['complexity_score'])
                with col4:
                    st.metric("Issues Found", len(result.issues))
                
                # Progress bars for metrics
                st.markdown("### 📈 Quality Metrics")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("Maintainability Index")
                    st.progress(result.metrics['maintainability_index'] / 100)
                    st.write(f"{result.metrics['maintainability_index']:.1f}/100")
                    
                    st.write("Documentation Coverage")
                    st.progress(result.metrics['documentation_coverage'] / 100)
                    st.write(f"{result.metrics['documentation_coverage']:.1f}%")
                
                with col2:
                    st.write("Test Coverage")
                    st.progress(result.metrics['test_coverage'] / 100)
                    st.write(f"{result.metrics['test_coverage']:.1f}%")
                    
                    st.write("Code Duplication")
                    st.progress(result.metrics['code_duplication'] / 100)
                    st.write(f"{result.metrics['code_duplication']:.1f}%")
                
                # Display summary
                st.markdown("### 📝 Summary")
                st.text(result.summary)
                
                # Display issues by severity
                st.markdown("### 🚨 Issues Detected")
                
                from co_creation_tools.code_assistant.code_reviewer import Severity
                
                for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
                    issues = result.get_issues_by_severity(severity)
                    if issues:
                        with st.expander(f"{severity.value.upper()} ({len(issues)} issues)"):
                            for issue in issues:
                                st.markdown(f"**Line {issue.line_number}** - {issue.category.value}")
                                st.write(f"❌ {issue.message}")
                                st.code(issue.code_snippet, language=language)
                                st.write(f"💡 {issue.suggestion}")
                                if issue.fixed_code:
                                    st.code(issue.fixed_code, language=language)
                                st.markdown("---")
            else:
                st.warning("Please paste code to review")
    
    with tab2:
        st.subheader("Refactoring Suggestions")
        
        code = st.text_area("Paste your code here:", height=300, key="refactor_code")
        target = st.selectbox("Refactoring Goal", ["readability", "performance", "testability"])
        
        if st.button("Get Suggestions"):
            if code:
                suggestions = reviewer.suggest_refactoring(code, target=target)
                
                st.success("✅ Suggestions generated!")
                
                st.markdown(f"### 🎯 Target: {suggestions['target'].title()}")
                st.metric("Estimated Improvement", f"{suggestions['estimated_improvement']}%")
                
                st.markdown("### 💡 Suggestions")
                for i, suggestion in enumerate(suggestions['suggestions'], 1):
                    st.write(f"{i}. {suggestion}")
            else:
                st.warning("Please paste code for refactoring suggestions")
    
    with tab3:
        st.subheader("Test Generation")
        
        code = st.text_area("Paste your code here:", height=300, key="test_gen_code")
        framework = st.selectbox("Testing Framework", ["pytest", "unittest"])
        
        if st.button("Generate Tests"):
            if code:
                with st.spinner("Generating tests..."):
                    tests = reviewer.generate_tests(code, framework=framework)
                
                st.success("✅ Tests generated!")
                
                st.markdown("### 🧪 Generated Test Code")
                st.code(tests, language="python")
                
                st.download_button(
                    label="📥 Download Tests",
                    data=tests,
                    file_name=f"test_generated.py",
                    mime="text/plain"
                )
            else:
                st.warning("Please paste code to generate tests")


if __name__ == "__main__":
    main()
