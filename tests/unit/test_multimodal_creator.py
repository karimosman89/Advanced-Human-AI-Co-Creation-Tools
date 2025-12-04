"""
Unit tests for Multimodal Creator
"""

import pytest
from co_creation_tools.creative_studio import MultimodalCreator
from co_creation_tools.creative_studio.multimodal_creator import Style


class TestMultimodalCreator:
    """Test suite for Multimodal Creator"""
    
    @pytest.fixture
    def creator(self, tmp_path):
        """Create Multimodal Creator instance"""
        return MultimodalCreator(workspace_dir=str(tmp_path))
    
    def test_initialization(self, creator):
        """Test creator initialization"""
        assert creator is not None
        assert creator.projects == {}
        assert creator.generation_history == []
    
    def test_create_project(self, creator):
        """Test project creation"""
        project = creator.create_project(
            name="Test Project",
            description="Test description"
        )
        
        assert project is not None
        assert project.name == "Test Project"
        assert project.description == "Test description"
        assert len(creator.projects) == 1
    
    def test_generate_text(self, creator):
        """Test text generation"""
        project = creator.create_project("Test", "Test")
        
        result = creator.generate_text(
            project_id=project.project_id,
            prompt="Test prompt",
            style=Style.PROFESSIONAL,
            num_variations=2
        )
        
        assert result is not None
        assert result['type'] == 'text'
        assert len(result['variations']) == 2
        assert result['prompt'] == "Test prompt"
    
    def test_generate_image_prompt(self, creator):
        """Test image prompt generation"""
        project = creator.create_project("Test", "Test")
        
        result = creator.generate_image_prompt(
            project_id=project.project_id,
            description="A beautiful sunset",
            style="photorealistic",
            aspect_ratio="16:9"
        )
        
        assert result is not None
        assert result['type'] == 'image_prompt'
        assert 'optimized_prompt' in result
        assert len(result['prompt_variations']) > 0
    
    def test_generate_code(self, creator):
        """Test code generation"""
        project = creator.create_project("Test", "Test")
        
        result = creator.generate_code(
            project_id=project.project_id,
            description="Data processing function",
            language="python"
        )
        
        assert result is not None
        assert result['type'] == 'code'
        assert result['language'] == 'python'
        assert 'code' in result
        assert 'documentation' in result
    
    def test_create_marketing_campaign(self, creator):
        """Test marketing campaign creation"""
        campaign = creator.create_marketing_campaign(
            product_name="Test Product",
            target_audience="Developers",
            key_message="Test message",
            channels=['social', 'email']
        )
        
        assert campaign is not None
        assert len(campaign.assets) > 0
        assert campaign.metadata['product'] == "Test Product"
    
    def test_get_project_summary(self, creator):
        """Test project summary"""
        project = creator.create_project("Test", "Test")
        creator.generate_text(
            project_id=project.project_id,
            prompt="Test",
            style=Style.PROFESSIONAL
        )
        
        summary = creator.get_project_summary(project.project_id)
        
        assert summary['project_id'] == project.project_id
        assert summary['total_assets'] == 1
        assert 'text' in summary['asset_breakdown']
