"""
Setup configuration for Advanced Human-AI Co-Creation Tools
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file) as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="co-creation-tools",
    version="1.0.0",
    author="Karim Osman",
    author_email="karim@example.com",
    description="Advanced tools for seamless human-AI collaboration in creative and problem-solving tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karimosman89/Advanced-Human-AI-Co-Creation-Tools",
    project_urls={
        "Bug Reports": "https://github.com/karimosman89/Advanced-Human-AI-Co-Creation-Tools/issues",
        "Source": "https://github.com/karimosman89/Advanced-Human-AI-Co-Creation-Tools",
        "Documentation": "https://github.com/karimosman89/Advanced-Human-AI-Co-Creation-Tools/docs",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "isort>=5.12.0",
            "pylint>=3.0.0",
            "pre-commit>=3.5.0",
        ],
        "docs": [
            "mkdocs>=1.5.3",
            "mkdocs-material>=9.4.10",
            "mkdocstrings[python]>=0.24.0",
        ],
        "api": [
            "openai>=1.3.0",
            "anthropic>=0.7.0",
            "cohere>=4.37",
        ],
    },
    entry_points={
        "console_scripts": [
            "co-create=co_creation_tools.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "artificial-intelligence",
        "machine-learning",
        "natural-language-processing",
        "code-generation",
        "creative-ai",
        "rag",
        "retrieval-augmented-generation",
        "code-review",
        "ai-assistant",
        "human-ai-collaboration",
    ],
)
