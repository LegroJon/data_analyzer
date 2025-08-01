"""
Setup script for Data Analyzer package.
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="data-analyzer",
    version="1.0.0",
    author="Jonathan Legro",
    author_email="jonathan@example.com",
    description="A professional-grade tool for parsing and analyzing military task data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LegroJon/data_analyzer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[],  # No external dependencies for core functionality
    extras_require={
        "dev": ["pytest>=7.0.0", "pytest-cov>=4.0.0"],
        "analytics": ["pandas>=1.5.0", "numpy>=1.21.0"],
        "docs": ["sphinx>=4.0.0", "sphinx-rtd-theme>=1.0.0"],
    },
    entry_points={
        "console_scripts": [
            "data-analyzer=src.task_parser:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
