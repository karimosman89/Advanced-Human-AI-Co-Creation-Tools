"""
Code Reviewer Demo: Security-Focused Code Review

This example demonstrates comprehensive code review with emphasis on security
vulnerability detection, performance analysis, and test generation.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from co_creation_tools.code_assistant import CodeReviewer
from co_creation_tools.code_assistant.code_reviewer import Severity, Category


def main():
    """Run Code Reviewer demo"""
    
    print("="*80)
    print("CODE REVIEWER DEMO: Security-Focused Code Review")
    print("="*80)
    
    # Initialize Code Reviewer
    print("\n💻 Initializing Code Reviewer (strict mode)...")
    reviewer = CodeReviewer(strict_mode=True)
    
    # Sample code with various issues
    sample_code = '''
import pickle
import subprocess
import os

# Security Issue: Hardcoded credentials
DATABASE_PASSWORD = "secret_password_123"
API_KEY = "sk-1234567890abcdef"

class DataProcessor:
    """Process and analyze data"""
    
    def __init__(self):
        self.data = []
    
    # Security Issue: Unsafe deserialization
    def load_data(self, filename):
        with open(filename, 'rb') as f:
            self.data = pickle.loads(f.read())
        return self.data
    
    # Security Issue: Command injection vulnerability
    def run_analysis(self, command):
        subprocess.call(command, shell=True)
    
    # Performance Issue: String concatenation in loop
    def generate_report(self, items):
        report = ""
        for item in items:
            report += str(item) + "\\n"
        return report
    
    # Best Practice Issue: Bare except
    def process_item(self, item):
        try:
            result = self.analyze(item)
            return result
        except:
            return None
    
    # Missing type hints and docstring
    def analyze(self, item):
        return item * 2

# Code Style Issue: Long line
def very_long_function_name_that_exceeds_reasonable_length(parameter1, parameter2, parameter3, parameter4, parameter5, parameter6):
    pass
'''
    
    # Perform comprehensive review
    print("\n🔍 Performing comprehensive code review...")
    result = reviewer.review_code(sample_code, "data_processor.py", "python")
    
    # Display summary
    print("\n" + "="*80)
    print("REVIEW SUMMARY")
    print("="*80)
    print(result.summary)
    
    # Display metrics
    print("\n" + "="*80)
    print("CODE QUALITY METRICS")
    print("="*80)
    
    metrics = result.metrics
    print(f"\n📊 Quality Grade: {metrics['grade']}")
    print(f"\n📏 Code Metrics:")
    print(f"   • Lines of Code: {metrics['lines_of_code']}")
    print(f"   • Complexity Score: {metrics['complexity_score']}")
    print(f"   • Maintainability Index: {metrics['maintainability_index']:.1f}/100")
    print(f"   • Test Coverage: {metrics['test_coverage']:.1f}%")
    print(f"   • Documentation Coverage: {metrics['documentation_coverage']:.1f}%")
    print(f"   • Code Duplication: {metrics['code_duplication']:.1f}%")
    
    # Display issues by severity
    print("\n" + "="*80)
    print("DETAILED ISSUES")
    print("="*80)
    
    severities = [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]
    
    for severity in severities:
        issues = result.get_issues_by_severity(severity)
        if issues:
            print(f"\n{'='*80}")
            print(f"{severity.value.upper()} SEVERITY ({len(issues)} issues)")
            print(f"{'='*80}")
            
            for i, issue in enumerate(issues, 1):
                print(f"\n{i}. Line {issue.line_number} - {issue.category.value}")
                print(f"   ❌ Issue: {issue.message}")
                print(f"   📄 Code: {issue.code_snippet}")
                print(f"   💡 Suggestion: {issue.suggestion}")
                if issue.fixed_code:
                    print(f"   ✅ Fix: {issue.fixed_code}")
    
    # Security-specific analysis
    print("\n" + "="*80)
    print("SECURITY ANALYSIS")
    print("="*80)
    
    security_issues = result.get_issues_by_category(Category.SECURITY)
    print(f"\n🚨 Security Issues Found: {len(security_issues)}")
    
    for issue in security_issues:
        print(f"\n• Line {issue.line_number}: {issue.message}")
        print(f"  Severity: {issue.severity.value.upper()}")
        print(f"  Suggestion: {issue.suggestion}")
    
    # Performance analysis
    print("\n" + "="*80)
    print("PERFORMANCE ANALYSIS")
    print("="*80)
    
    perf_issues = result.get_issues_by_category(Category.PERFORMANCE)
    print(f"\n⚡ Performance Issues Found: {len(perf_issues)}")
    
    for issue in perf_issues:
        print(f"\n• Line {issue.line_number}: {issue.message}")
        print(f"  Suggestion: {issue.suggestion}")
    
    # Generate tests
    print("\n" + "="*80)
    print("TEST GENERATION")
    print("="*80)
    
    print("\n🧪 Generating unit tests...")
    tests = reviewer.generate_tests(sample_code, framework="pytest")
    
    print(f"\n📄 Generated Test Code:")
    print(tests[:800] + "\n... [truncated]")
    
    # Save tests
    test_file = "test_generated.py"
    with open(test_file, 'w') as f:
        f.write(tests)
    print(f"\n💾 Full test file saved to: {test_file}")
    
    # Refactoring suggestions
    print("\n" + "="*80)
    print("REFACTORING SUGGESTIONS")
    print("="*80)
    
    targets = ["security", "performance", "testability"]
    
    for target in targets:
        print(f"\n🎯 {target.upper()} Refactoring:")
        suggestions = reviewer.suggest_refactoring(sample_code, target=target)
        
        print(f"   Estimated Improvement: {suggestions['estimated_improvement']}%")
        print(f"   Suggestions:")
        for i, suggestion in enumerate(suggestions['suggestions'], 1):
            print(f"      {i}. {suggestion}")
    
    # Export report
    print("\n" + "="*80)
    print("EXPORT REPORT")
    print("="*80)
    
    report_file = "code_review_report.md"
    print(f"\n📝 Exporting detailed report...")
    reviewer.export_report(result, report_file, format="markdown")
    print(f"✅ Report saved to: {report_file}")
    
    # Summary statistics
    print("\n" + "="*80)
    print("FINAL STATISTICS")
    print("="*80)
    
    print(f"\n📊 Review Statistics:")
    print(f"   • Total Issues: {len(result.issues)}")
    print(f"   • Critical: {len(result.get_issues_by_severity(Severity.CRITICAL))}")
    print(f"   • High: {len(result.get_issues_by_severity(Severity.HIGH))}")
    print(f"   • Medium: {len(result.get_issues_by_severity(Severity.MEDIUM))}")
    print(f"   • Low: {len(result.get_issues_by_severity(Severity.LOW))}")
    print(f"\n   • Security Issues: {len(security_issues)}")
    print(f"   • Performance Issues: {len(perf_issues)}")
    print(f"\n   • Quality Grade: {metrics['grade']}")
    print(f"   • Maintainability: {metrics['maintainability_index']:.1f}/100")
    
    print("\n" + "="*80)
    print("✅ Demo completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()
