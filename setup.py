#!/usr/bin/env python3
"""
Setup script for Modelo X Framework v2.0
Hyperdimensional Theory of Universal Complexity
"""

from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="modelo-x-framework",
    version="2.0.0",
    author="Tiago Hanna",
    author_email="tiago@example.com",  # Update with real email
    description="A hyperdimensional framework for universal complexity analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tiagohanna123/o",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "notebooks": [
            "jupyter>=1.0.0",
            "ipywidgets>=7.0.0",
        ],
        "performance": [
            "numba>=0.54.0",
            "cython>=0.29.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "modelo-x=src.o_v2:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.html", "*.md", "*.json", "*.csv", "*.png"],
    },
    zip_safe=False,
)