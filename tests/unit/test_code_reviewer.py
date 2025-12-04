"""
Unit tests for Code Reviewer
"""

import pytest
from co_creation_tools.code_assistant import CodeReviewer
from co_creation_tools.code_assistant.code_reviewer import Severity, Category


class TestCodeReviewer:
    """Test suite for Code Reviewer"""
    
    @pytest.fixture
    def reviewer(self):
        """Create Code Reviewer instance"""
        return CodeReviewer(strict_mode=False)
    
    @pytest.fixture
    def sample_code(self):
        """Sample code for testing"""
        return """
def calculate(x, y):
    result = x + y
    return result

def process_data(items):
    result = ""
    for item in items:
        result += str(item)
    return result
"""
    
    @pytest.fixture
    def vulnerable_code(self):
        """Vulnerable code for security testing"""
        return """
import pickle

password = "hardcoded_password_123"

def load_data(filename):
    with open(filename, 'rb') as f:
        return pickle.loads(f.read())

def run_command(user_input):
    import subprocess
    subprocess.call(user_input, shell=True)
"""
    
    def test_initialization(self, reviewer):
        """Test reviewer initialization"""
        assert reviewer is not None
        assert reviewer.strict_mode is False
        assert reviewer.review_history == []
    
    def test_review_code_basic(self, reviewer, sample_code):
        """Test basic code review"""
        result = reviewer.review_code(sample_code, "test.py", "python")
        
        assert result is not None
        assert result.file_name == "test.py"
        assert result.language == "python"
        assert result.total_lines > 0
        assert 'grade' in result.metrics
    
    def test_security_check(self, reviewer, vulnerable_code):
        """Test security vulnerability detection"""
        result = reviewer.review_code(vulnerable_code, "vulnerable.py", "python")
        
        security_issues = result.get_issues_by_category(Category.SECURITY)
        assert len(security_issues) > 0
        
        critical_issues = result.get_issues_by_severity(Severity.CRITICAL)
        assert len(critical_issues) > 0
    
    def test_performance_check(self, reviewer, sample_code):
        """Test performance issue detection"""
        result = reviewer.review_code(sample_code, "test.py", "python")
        
        perf_issues = result.get_issues_by_category(Category.PERFORMANCE)
        # Should detect string concatenation in loop
        assert any('concatenation' in issue.message.lower() for issue in result.issues)
    
    def test_calculate_metrics(self, reviewer, sample_code):
        """Test metrics calculation"""
        result = reviewer.review_code(sample_code, "test.py", "python")
        
        assert 'lines_of_code' in result.metrics
        assert 'complexity_score' in result.metrics
        assert 'maintainability_index' in result.metrics
        assert result.metrics['lines_of_code'] > 0
    
    def test_generate_tests(self, reviewer, sample_code):
        """Test test generation"""
        tests = reviewer.generate_tests(sample_code, framework="pytest")
        
        assert tests is not None
        assert 'def test_' in tests
        assert 'pytest' in tests
    
    def test_suggest_refactoring(self, reviewer, sample_code):
        """Test refactoring suggestions"""
        suggestions = reviewer.suggest_refactoring(sample_code, target="performance")
        
        assert suggestions is not None
        assert 'target' in suggestions
        assert suggestions['target'] == 'performance'
        assert len(suggestions['suggestions']) > 0
    
    def test_strict_mode(self):
        """Test strict mode enables additional checks"""
        reviewer = CodeReviewer(strict_mode=True)
        
        code = "def test():\n    return None"
        result = reviewer.review_code(code, "test.py", "python")
        
        # Strict mode should find more issues (e.g., missing type hints)
        assert len(result.issues) > 0
