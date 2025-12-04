"""
AI-Powered Code Review and Pair Programming Assistant

This module provides intelligent code review, suggestions, and pair programming capabilities.

Use Cases:
- Automated code review and quality analysis
- Security vulnerability detection
- Performance optimization suggestions
- Best practices enforcement
- Real-time pair programming assistance
- Test generation and coverage analysis
"""

import re
import ast
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Category(Enum):
    """Issue categories"""
    SECURITY = "security"
    PERFORMANCE = "performance"
    BUG = "bug"
    CODE_STYLE = "code_style"
    BEST_PRACTICE = "best_practice"
    DOCUMENTATION = "documentation"
    TESTING = "testing"


@dataclass
class CodeIssue:
    """Represents a code issue found during review"""
    severity: Severity
    category: Category
    line_number: int
    message: str
    suggestion: str
    code_snippet: str
    fixed_code: Optional[str] = None
    
    def __str__(self) -> str:
        return f"[{self.severity.value.upper()}] Line {self.line_number}: {self.message}"


@dataclass
class ReviewResult:
    """Complete code review result"""
    file_name: str
    language: str
    total_lines: int
    issues: List[CodeIssue]
    metrics: Dict[str, Any]
    summary: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def get_issues_by_severity(self, severity: Severity) -> List[CodeIssue]:
        """Get issues filtered by severity"""
        return [issue for issue in self.issues if issue.severity == severity]
    
    def get_issues_by_category(self, category: Category) -> List[CodeIssue]:
        """Get issues filtered by category"""
        return [issue for issue in self.issues if issue.category == category]
    
    def get_critical_count(self) -> int:
        """Get count of critical issues"""
        return len(self.get_issues_by_severity(Severity.CRITICAL))


@dataclass
class CodeMetrics:
    """Code quality metrics"""
    lines_of_code: int
    complexity_score: float
    maintainability_index: float
    test_coverage: float
    documentation_coverage: float
    code_duplication: float
    
    def get_grade(self) -> str:
        """Get overall quality grade"""
        avg_score = (
            self.maintainability_index * 0.3 +
            self.test_coverage * 0.3 +
            self.documentation_coverage * 0.2 +
            (100 - self.code_duplication) * 0.2
        )
        
        if avg_score >= 90:
            return "A+"
        elif avg_score >= 80:
            return "A"
        elif avg_score >= 70:
            return "B"
        elif avg_score >= 60:
            return "C"
        else:
            return "D"


class CodeReviewer:
    """
    AI-powered code review and pair programming assistant.
    
    Features:
    - Automated code review with severity classification
    - Security vulnerability detection
    - Performance optimization suggestions
    - Best practices enforcement
    - Test generation recommendations
    - Documentation completeness analysis
    - Refactoring suggestions
    
    Example:
        >>> reviewer = CodeReviewer()
        >>> result = reviewer.review_code(python_code, "example.py")
        >>> print(f"Found {len(result.issues)} issues")
        >>> for issue in result.issues:
        ...     print(issue)
    """
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize the Code Reviewer.
        
        Args:
            strict_mode: Enable strict mode for more rigorous checks
        """
        self.strict_mode = strict_mode
        self.review_history: List[ReviewResult] = []
        self.knowledge_base = self._load_knowledge_base()
        
        print(f"[Code Reviewer] Initialized (strict_mode: {strict_mode})")
    
    def _load_knowledge_base(self) -> Dict:
        """Load code review knowledge base"""
        return {
            'security_patterns': [
                r'eval\s*\(',
                r'exec\s*\(',
                r'input\s*\(',
                r'__import__',
                r'pickle\.loads',
            ],
            'performance_patterns': [
                r'\.append\s*\(.*\)\s+in\s+for',  # List append in loop
                r'\+\=.*str',  # String concatenation in loop
            ],
            'best_practices': {
                'python': [
                    'Use list comprehensions instead of loops where appropriate',
                    'Follow PEP 8 style guidelines',
                    'Use type hints for better code clarity',
                    'Implement proper exception handling',
                    'Add docstrings to all public methods'
                ]
            }
        }
    
    def review_code(self, code: str, filename: str, language: str = "python") -> ReviewResult:
        """
        Perform comprehensive code review.
        
        Args:
            code: Source code to review
            filename: Name of the file
            language: Programming language
            
        Returns:
            ReviewResult with issues and metrics
        """
        print(f"[Code Reviewer] Reviewing: {filename} ({language})")
        
        issues = []
        
        # Perform different types of analysis
        issues.extend(self._check_security(code, language))
        issues.extend(self._check_performance(code, language))
        issues.extend(self._check_code_style(code, language))
        issues.extend(self._check_best_practices(code, language))
        issues.extend(self._check_documentation(code, language))
        
        # Calculate metrics
        metrics = self._calculate_metrics(code, language)
        
        # Generate summary
        summary = self._generate_summary(issues, metrics)
        
        result = ReviewResult(
            file_name=filename,
            language=language,
            total_lines=len(code.split('\n')),
            issues=issues,
            metrics=metrics,
            summary=summary
        )
        
        self.review_history.append(result)
        
        print(f"[Code Reviewer] Found {len(issues)} issues")
        print(f"[Code Reviewer] Quality Grade: {metrics.get('grade', 'N/A')}")
        
        return result
    
    def _check_security(self, code: str, language: str) -> List[CodeIssue]:
        """Check for security vulnerabilities"""
        issues = []
        
        if language == "python":
            # Check for dangerous functions
            dangerous_patterns = {
                r'eval\s*\(': 'Avoid using eval() - it can execute arbitrary code',
                r'exec\s*\(': 'Avoid using exec() - it can execute arbitrary code',
                r'pickle\.loads': 'pickle.loads can execute arbitrary code - use json instead',
                r'subprocess\.(call|run|Popen).*shell\s*=\s*True': 'Avoid shell=True in subprocess - prone to injection attacks',
                r'os\.system\s*\(': 'Avoid os.system() - use subprocess with proper escaping',
            }
            
            for line_num, line in enumerate(code.split('\n'), 1):
                for pattern, message in dangerous_patterns.items():
                    if re.search(pattern, line):
                        issues.append(CodeIssue(
                            severity=Severity.CRITICAL,
                            category=Category.SECURITY,
                            line_number=line_num,
                            message=message,
                            suggestion="Use safer alternatives with proper input validation",
                            code_snippet=line.strip(),
                            fixed_code=self._suggest_security_fix(line, pattern)
                        ))
            
            # Check for hardcoded credentials
            credential_patterns = [
                r'password\s*=\s*["\'][^"\']+["\']',
                r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']',
                r'token\s*=\s*["\'][^"\']+["\']',
            ]
            
            for line_num, line in enumerate(code.split('\n'), 1):
                for pattern in credential_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(CodeIssue(
                            severity=Severity.HIGH,
                            category=Category.SECURITY,
                            line_number=line_num,
                            message="Hardcoded credentials detected",
                            suggestion="Use environment variables or secure credential management",
                            code_snippet=line.strip(),
                            fixed_code="# Use: password = os.getenv('PASSWORD')"
                        ))
        
        return issues
    
    def _check_performance(self, code: str, language: str) -> List[CodeIssue]:
        """Check for performance issues"""
        issues = []
        
        if language == "python":
            lines = code.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # Check for string concatenation in loops
                if 'for ' in line or 'while ' in line:
                    # Look ahead for string concatenation
                    if line_num < len(lines):
                        next_lines = ' '.join(lines[line_num:min(line_num+5, len(lines))])
                        if re.search(r'\+=.*["\']', next_lines):
                            issues.append(CodeIssue(
                                severity=Severity.MEDIUM,
                                category=Category.PERFORMANCE,
                                line_number=line_num,
                                message="String concatenation in loop detected",
                                suggestion="Use list and join() or io.StringIO for better performance",
                                code_snippet=line.strip(),
                                fixed_code="# result = ''.join(string_list)"
                            ))
                
                # Check for list append in comprehension-able situation
                if '.append(' in line and 'for ' in line:
                    issues.append(CodeIssue(
                        severity=Severity.LOW,
                        category=Category.PERFORMANCE,
                        line_number=line_num,
                        message="Consider using list comprehension",
                        suggestion="List comprehensions are generally faster than append in loops",
                        code_snippet=line.strip(),
                        fixed_code="# result = [item for item in iterable]"
                    ))
                
                # Check for unnecessary list copies
                if re.search(r'list\s*\(.*\.keys\(\)\)', line):
                    issues.append(CodeIssue(
                        severity=Severity.LOW,
                        category=Category.PERFORMANCE,
                        line_number=line_num,
                        message="Unnecessary list() call on dict.keys()",
                        suggestion="dict.keys() already returns a view, no need for list()",
                        code_snippet=line.strip(),
                        fixed_code=line.replace('list(', '').replace('.keys())', '.keys()')
                    ))
        
        return issues
    
    def _check_code_style(self, code: str, language: str) -> List[CodeIssue]:
        """Check code style and formatting"""
        issues = []
        
        if language == "python":
            lines = code.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # Check line length (PEP 8: 79 characters)
                if len(line) > 100:
                    issues.append(CodeIssue(
                        severity=Severity.LOW,
                        category=Category.CODE_STYLE,
                        line_number=line_num,
                        message=f"Line too long ({len(line)} characters)",
                        suggestion="PEP 8 recommends maximum line length of 79-100 characters",
                        code_snippet=line[:50] + "...",
                        fixed_code="# Consider breaking into multiple lines"
                    ))
                
                # Check for improper spacing around operators
                if re.search(r'\w+[+\-*/]=\w+', line) and '==' not in line:
                    issues.append(CodeIssue(
                        severity=Severity.LOW,
                        category=Category.CODE_STYLE,
                        line_number=line_num,
                        message="Missing spaces around operator",
                        suggestion="Add spaces around operators for readability",
                        code_snippet=line.strip(),
                        fixed_code=re.sub(r'(\w+)([+\-*/]=)(\w+)', r'\1 \2 \3', line.strip())
                    ))
                
                # Check for missing whitespace after comma
                if re.search(r',\w', line) and not re.search(r'["\'],', line):
                    issues.append(CodeIssue(
                        severity=Severity.LOW,
                        category=Category.CODE_STYLE,
                        line_number=line_num,
                        message="Missing whitespace after comma",
                        suggestion="Add space after comma for better readability",
                        code_snippet=line.strip(),
                        fixed_code=re.sub(r',(\w)', r', \1', line.strip())
                    ))
        
        return issues
    
    def _check_best_practices(self, code: str, language: str) -> List[CodeIssue]:
        """Check for best practices violations"""
        issues = []
        
        if language == "python":
            lines = code.split('\n')
            
            # Check for broad exception handling
            for line_num, line in enumerate(lines, 1):
                if re.search(r'except\s*:', line) or re.search(r'except\s+Exception\s*:', line):
                    issues.append(CodeIssue(
                        severity=Severity.MEDIUM,
                        category=Category.BEST_PRACTICE,
                        line_number=line_num,
                        message="Catching too broad exception",
                        suggestion="Catch specific exceptions instead of bare except or Exception",
                        code_snippet=line.strip(),
                        fixed_code="# except SpecificError:"
                    ))
                
                # Check for mutable default arguments
                if re.search(r'def\s+\w+\s*\([^)]*=\s*\[', line) or re.search(r'def\s+\w+\s*\([^)]*=\s*\{', line):
                    issues.append(CodeIssue(
                        severity=Severity.HIGH,
                        category=Category.BUG,
                        line_number=line_num,
                        message="Mutable default argument detected",
                        suggestion="Use None as default and initialize inside function",
                        code_snippet=line.strip(),
                        fixed_code="# def func(arg=None):\n#     if arg is None:\n#         arg = []"
                    ))
                
                # Check for == comparison with None, True, False
                if re.search(r'==\s*(None|True|False)', line) or re.search(r'(None|True|False)\s*==', line):
                    issues.append(CodeIssue(
                        severity=Severity.LOW,
                        category=Category.BEST_PRACTICE,
                        line_number=line_num,
                        message="Use 'is' for None, True, False comparisons",
                        suggestion="Use 'is' or 'is not' instead of '==' for identity checks",
                        code_snippet=line.strip(),
                        fixed_code=line.strip().replace('==', 'is')
                    ))
            
            # Check for missing type hints (if strict mode)
            if self.strict_mode:
                for line_num, line in enumerate(lines, 1):
                    if re.match(r'\s*def\s+\w+\s*\([^)]*\)\s*:', line):
                        if '->' not in line:
                            issues.append(CodeIssue(
                                severity=Severity.INFO,
                                category=Category.BEST_PRACTICE,
                                line_number=line_num,
                                message="Missing return type hint",
                                suggestion="Add return type hint for better code clarity",
                                code_snippet=line.strip(),
                                fixed_code=line.strip().replace('):', ') -> ReturnType:')
                            ))
        
        return issues
    
    def _check_documentation(self, code: str, language: str) -> List[CodeIssue]:
        """Check documentation completeness"""
        issues = []
        
        if language == "python":
            lines = code.split('\n')
            
            # Check for missing docstrings
            for line_num, line in enumerate(lines, 1):
                if re.match(r'\s*def\s+\w+', line) or re.match(r'\s*class\s+\w+', line):
                    # Check if next non-empty line is a docstring
                    has_docstring = False
                    for next_line_num in range(line_num, min(line_num + 3, len(lines))):
                        next_line = lines[next_line_num]
                        if '"""' in next_line or "'''" in next_line:
                            has_docstring = True
                            break
                        if next_line.strip() and not next_line.strip().startswith('#'):
                            break
                    
                    if not has_docstring:
                        entity_type = "function" if "def " in line else "class"
                        issues.append(CodeIssue(
                            severity=Severity.LOW,
                            category=Category.DOCUMENTATION,
                            line_number=line_num,
                            message=f"Missing docstring for {entity_type}",
                            suggestion=f"Add docstring to document {entity_type} purpose and parameters",
                            code_snippet=line.strip(),
                            fixed_code=f'{line.strip()}\n    """Add description here"""'
                        ))
        
        return issues
    
    def _suggest_security_fix(self, line: str, pattern: str) -> str:
        """Suggest security fix for problematic code"""
        if 'eval' in pattern:
            return "# Use ast.literal_eval() for safe evaluation of literals"
        elif 'exec' in pattern:
            return "# Restructure code to avoid exec(), use functions or imports"
        elif 'pickle' in pattern:
            return "# Use json.loads() for safe deserialization"
        elif 'subprocess' in pattern:
            return "# subprocess.run(['cmd', 'arg'], shell=False, check=True)"
        else:
            return "# Implement proper input validation and sanitization"
    
    def _calculate_metrics(self, code: str, language: str) -> Dict[str, Any]:
        """Calculate code quality metrics"""
        lines = [line for line in code.split('\n') if line.strip()]
        total_lines = len(lines)
        
        # Calculate complexity (simplified)
        complexity = 1  # Base complexity
        complexity += len(re.findall(r'\bif\b', code))
        complexity += len(re.findall(r'\bfor\b', code))
        complexity += len(re.findall(r'\bwhile\b', code))
        complexity += len(re.findall(r'\band\b|\bor\b', code))
        
        # Calculate maintainability index (simplified, 0-100 scale)
        # Formula: 171 - 5.2 * ln(V) - 0.23 * G - 16.2 * ln(LOC)
        # Simplified version
        import math
        volume = total_lines * 10  # Simplified volume
        maintainability = max(0, min(100, 171 - 5.2 * math.log(volume + 1) - 0.23 * complexity))
        
        # Estimate test coverage (simplified - would need actual test analysis)
        has_tests = 'def test_' in code or 'class Test' in code
        test_coverage = 80.0 if has_tests else 20.0
        
        # Estimate documentation coverage
        docstrings = len(re.findall(r'""".*?"""', code, re.DOTALL))
        functions = len(re.findall(r'def \w+', code))
        classes = len(re.findall(r'class \w+', code))
        doc_coverage = (docstrings / max(functions + classes, 1)) * 100
        doc_coverage = min(100, doc_coverage)
        
        # Estimate code duplication (simplified)
        lines_set = set(line.strip() for line in lines if line.strip())
        duplication = max(0, (1 - len(lines_set) / max(len(lines), 1)) * 100)
        
        metrics_obj = CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            maintainability_index=maintainability,
            test_coverage=test_coverage,
            documentation_coverage=doc_coverage,
            code_duplication=duplication
        )
        
        return {
            'lines_of_code': total_lines,
            'complexity_score': complexity,
            'maintainability_index': round(maintainability, 2),
            'test_coverage': round(test_coverage, 2),
            'documentation_coverage': round(doc_coverage, 2),
            'code_duplication': round(duplication, 2),
            'grade': metrics_obj.get_grade()
        }
    
    def _generate_summary(self, issues: List[CodeIssue], metrics: Dict) -> str:
        """Generate review summary"""
        critical = sum(1 for i in issues if i.severity == Severity.CRITICAL)
        high = sum(1 for i in issues if i.severity == Severity.HIGH)
        medium = sum(1 for i in issues if i.severity == Severity.MEDIUM)
        low = sum(1 for i in issues if i.severity == Severity.LOW)
        
        summary = f"""Code Review Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Quality Grade: {metrics.get('grade', 'N/A')}

Issues Found: {len(issues)}
  • Critical: {critical}
  • High: {high}
  • Medium: {medium}
  • Low: {low}

Metrics:
  • Lines of Code: {metrics['lines_of_code']}
  • Complexity Score: {metrics['complexity_score']}
  • Maintainability: {metrics['maintainability_index']:.1f}/100
  • Test Coverage: {metrics['test_coverage']:.1f}%
  • Documentation: {metrics['documentation_coverage']:.1f}%

Recommendations:
"""
        
        if critical > 0:
            summary += f"  ⚠️  Address {critical} critical security/bug issues immediately\n"
        if high > 0:
            summary += f"  ⚡ Resolve {high} high-priority issues\n"
        if metrics['test_coverage'] < 60:
            summary += "  📝 Increase test coverage (target: 80%+)\n"
        if metrics['documentation_coverage'] < 70:
            summary += "  📚 Add missing documentation\n"
        if metrics['complexity_score'] > 20:
            summary += "  🔧 Refactor complex functions to reduce complexity\n"
        
        return summary
    
    def suggest_refactoring(self, code: str, target: str = "readability") -> Dict:
        """
        Suggest code refactoring improvements.
        
        Args:
            code: Source code to analyze
            target: Refactoring goal (readability, performance, testability)
            
        Returns:
            Dictionary with refactoring suggestions
        """
        suggestions = {
            'target': target,
            'suggestions': [],
            'estimated_improvement': 0
        }
        
        if target == "readability":
            suggestions['suggestions'] = [
                "Break long functions into smaller, single-purpose functions",
                "Use descriptive variable names instead of abbreviations",
                "Add docstrings and comments for complex logic",
                "Use type hints for better code clarity",
                "Follow consistent naming conventions"
            ]
            suggestions['estimated_improvement'] = 25
        
        elif target == "performance":
            suggestions['suggestions'] = [
                "Use list comprehensions instead of loops where appropriate",
                "Replace string concatenation with join() for multiple strings",
                "Cache expensive computations",
                "Use generators for large datasets",
                "Profile and optimize hot paths"
            ]
            suggestions['estimated_improvement'] = 30
        
        elif target == "testability":
            suggestions['suggestions'] = [
                "Reduce function complexity and dependencies",
                "Use dependency injection for better mocking",
                "Separate I/O operations from business logic",
                "Make functions pure where possible",
                "Add clear assertions and error messages"
            ]
            suggestions['estimated_improvement'] = 35
        
        print(f"[Code Reviewer] Generated {len(suggestions['suggestions'])} refactoring suggestions")
        
        return suggestions
    
    def generate_tests(self, code: str, framework: str = "pytest") -> str:
        """
        Generate unit tests for the provided code.
        
        Args:
            code: Source code to generate tests for
            framework: Testing framework (pytest, unittest)
            
        Returns:
            Generated test code
        """
        print(f"[Code Reviewer] Generating {framework} tests")
        
        # Extract function and class names
        functions = re.findall(r'def\s+(\w+)\s*\([^)]*\)', code)
        classes = re.findall(r'class\s+(\w+)', code)
        
        if framework == "pytest":
            test_code = f'''"""
Unit tests generated by AI Code Reviewer

Run with: pytest test_generated.py
"""

import pytest
from unittest.mock import Mock, patch

# Import your module here
# from your_module import *


'''
            # Generate tests for functions
            for func_name in functions:
                if not func_name.startswith('_'):  # Skip private functions
                    test_code += f'''
def test_{func_name}_basic():
    """Test basic functionality of {func_name}"""
    # Arrange
    # TODO: Set up test data
    
    # Act
    # result = {func_name}(test_input)
    
    # Assert
    # assert result == expected_output
    pass


def test_{func_name}_edge_cases():
    """Test edge cases for {func_name}"""
    # TODO: Test edge cases like empty input, None, etc.
    pass


def test_{func_name}_error_handling():
    """Test error handling in {func_name}"""
    # TODO: Test exception handling
    with pytest.raises(ValueError):
        pass  # {func_name}(invalid_input)


'''
            
            # Generate tests for classes
            for class_name in classes:
                test_code += f'''
class Test{class_name}:
    """Test suite for {class_name}"""
    
    @pytest.fixture
    def {class_name.lower()}_instance(self):
        """Fixture to create {class_name} instance"""
        return {class_name}()
    
    def test_initialization(self, {class_name.lower()}_instance):
        """Test {class_name} initialization"""
        assert {class_name.lower()}_instance is not None
        # TODO: Add more initialization checks
    
    def test_main_functionality(self, {class_name.lower()}_instance):
        """Test main functionality of {class_name}"""
        # TODO: Implement test
        pass


'''
        
        else:  # unittest
            test_code = f'''"""
Unit tests generated by AI Code Reviewer

Run with: python -m unittest test_generated.py
"""

import unittest
from unittest.mock import Mock, patch

# Import your module here
# from your_module import *


'''
            for func_name in functions:
                if not func_name.startswith('_'):
                    test_code += f'''
class Test{func_name.title()}(unittest.TestCase):
    """Test cases for {func_name}"""
    
    def setUp(self):
        """Set up test fixtures"""
        pass
    
    def tearDown(self):
        """Clean up after tests"""
        pass
    
    def test_{func_name}_basic(self):
        """Test basic functionality"""
        # TODO: Implement test
        pass
    
    def test_{func_name}_edge_cases(self):
        """Test edge cases"""
        # TODO: Implement test
        pass


'''
        
        return test_code
    
    def export_report(self, result: ReviewResult, filepath: str, format: str = "markdown") -> None:
        """
        Export review results to file.
        
        Args:
            result: ReviewResult to export
            filepath: Output file path
            format: Export format (markdown, html, json)
        """
        if format == "markdown":
            report = self._generate_markdown_report(result)
        elif format == "json":
            import json
            report = json.dumps({
                'file_name': result.file_name,
                'language': result.language,
                'total_lines': result.total_lines,
                'issues': [str(issue) for issue in result.issues],
                'metrics': result.metrics,
                'summary': result.summary,
                'timestamp': result.timestamp
            }, indent=2)
        else:
            report = result.summary
        
        with open(filepath, 'w') as f:
            f.write(report)
        
        print(f"[Code Reviewer] Report exported to: {filepath}")
    
    def _generate_markdown_report(self, result: ReviewResult) -> str:
        """Generate markdown report"""
        report = f"""# Code Review Report: {result.file_name}

**Language**: {result.language}  
**Total Lines**: {result.total_lines}  
**Quality Grade**: {result.metrics.get('grade', 'N/A')}  
**Review Date**: {result.timestamp}

---

{result.summary}

---

## Detailed Issues

"""
        
        # Group issues by severity
        for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
            issues = result.get_issues_by_severity(severity)
            if issues:
                report += f"\n### {severity.value.upper()} Issues ({len(issues)})\n\n"
                for issue in issues:
                    report += f"""#### Line {issue.line_number} - {issue.category.value}

**Issue**: {issue.message}

**Code**:
```python
{issue.code_snippet}
```

**Suggestion**: {issue.suggestion}

"""
                    if issue.fixed_code:
                        report += f"""**Proposed Fix**:
```python
{issue.fixed_code}
```

"""
                    report += "---\n\n"
        
        report += "## End of Report\n"
        
        return report


# Example usage and real-world scenarios
if __name__ == "__main__":
    # Initialize Code Reviewer
    reviewer = CodeReviewer(strict_mode=True)
    
    print("="*80)
    print("SCENARIO 1: Security Vulnerability Detection")
    print("="*80)
    
    # Sample code with security issues
    vulnerable_code = '''
import pickle
import subprocess

def load_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.loads(f.read())  # Security risk!
    return data

def run_command(user_input):
    # Dangerous: shell injection vulnerability
    subprocess.call(user_input, shell=True)

password = "hardcoded_secret_123"  # Security risk!
api_key = "sk-1234567890"  # Security risk!
'''
    
    result = reviewer.review_code(vulnerable_code, "vulnerable.py")
    print(result.summary)
    
    critical_issues = result.get_issues_by_severity(Severity.CRITICAL)
    print(f"\n🚨 Critical Security Issues: {len(critical_issues)}")
    for issue in critical_issues:
        print(f"  - {issue}")
    
    print("\n" + "="*80)
    print("SCENARIO 2: Performance Optimization")
    print("="*80)
    
    performance_code = '''
def process_data(items):
    result = ""
    for item in items:
        result += str(item) + ","  # Inefficient string concatenation!
    
    processed = []
    for item in items:
        processed.append(item * 2)  # Could use list comprehension
    
    return result, processed

def get_keys(data):
    return list(data.keys())  # Unnecessary list() call
'''
    
    result2 = reviewer.review_code(performance_code, "performance.py")
    perf_issues = result2.get_issues_by_category(Category.PERFORMANCE)
    print(f"\n⚡ Performance Issues Found: {len(perf_issues)}")
    for issue in perf_issues:
        print(f"\n{issue}")
        print(f"   Suggestion: {issue.suggestion}")
    
    print("\n" + "="*80)
    print("SCENARIO 3: Test Generation")
    print("="*80)
    
    sample_code = '''
class Calculator:
    def add(self, a, b):
        return a + b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''
    
    test_code = reviewer.generate_tests(sample_code, framework="pytest")
    print("\nGenerated Test Code:")
    print(test_code[:500] + "...\n")
    
    print("="*80)
    print("SCENARIO 4: Refactoring Suggestions")
    print("="*80)
    
    refactoring = reviewer.suggest_refactoring(sample_code, target="testability")
    print(f"\nRefactoring Goal: {refactoring['target']}")
    print(f"Estimated Improvement: {refactoring['estimated_improvement']}%")
    print("\nSuggestions:")
    for i, suggestion in enumerate(refactoring['suggestions'], 1):
        print(f"  {i}. {suggestion}")
