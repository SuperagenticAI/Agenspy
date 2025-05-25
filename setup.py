#!/usr/bin/env python3  
"""Setup script for Agentic-DSPy."""  
  
from setuptools import setup, find_packages  
  
with open("README.md", "r", encoding="utf-8") as fh:  
    long_description = fh.read()  
  
with open("requirements.txt", "r", encoding="utf-8") as fh:  
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]  
  
setup(  
    name="agentic-dspy",  
    version="0.1.0",  
    author="Shashi Jagtap",  
    author_email="shashi@super-agentic.ai",  
    description="Protocol-first AI agent framework built on DSPy",  
    long_description=long_description,  
    long_description_content_type="text/markdown",  
    url="https://github.com/superagenticai/agentic-dspy",  
    packages=find_packages(),  
    classifiers=[  
        "Development Status :: 3 - Alpha",  
        "Intended Audience :: Developers",  
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",  
        "Programming Language :: Python :: 3",  
        "Programming Language :: Python :: 3.9",  
        "Programming Language :: Python :: 3.10",  
        "Programming Language :: Python :: 3.11",  
    ],  
    python_requires=">=3.9",  
    install_requires=requirements,  
    extras_require={  
        "mcp": ["mcp>=1.0.0"],  
        "dev": ["pytest>=6.2.5", "black", "ruff", "mypy"],  
        "examples": ["openai>=1.0.0", "requests>=2.31.0"],  
    },  
)