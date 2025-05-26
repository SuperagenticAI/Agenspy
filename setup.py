#!/usr/bin/env python3
"""Setup script for Agenspy."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define all dependencies directly here
install_requires = [
    "dspy",
    "pydantic>=2.0",
    "fastapi>=0.100.0",
    "uvicorn>=0.20.0",
    "websockets>=11.0",
    "asyncio",
    "typing-extensions",
    "click>=8.0",
    "pyyaml>=6.0",
]

setup(
    name="agenspy",
    version="0.1.0",
    author="Agenspy Contributors",
    author_email="shashikant@super-agentic.ai",
    description="Protocol-first AI agent framework built on DSPy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/superagenticai/agenspy",
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
    install_requires=install_requires,  # Use the defined list here
    extras_require={
        "mcp": ["mcp>=1.0.0"],
        "dev": ["pytest>=6.2.5", "black", "ruff", "mypy", "pre-commit>=3.0.0"],
        "examples": ["openai>=1.0.0", "requests>=2.31.0"],
    },
    entry_points={
        "console_scripts": [
            "agenspy = agenspy.cli.main:main",
        ],
    },
)
