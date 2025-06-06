#!/usr/bin/env python3
"""
Setup-Skript für das Apfel QML-System

Installiert das Paket und alle Dependencies für lokale Entwicklung
oder Distribution.
"""

from setuptools import setup, find_packages
import os


def read_file(filename):
    """Liest den Inhalt einer Datei."""
    with open(os.path.join(os.path.dirname(__file__), filename), 'r', encoding='utf-8') as f:
        return f.read()


def read_requirements(filename):
    """Liest Requirements aus einer Datei."""
    requirements = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('-r'):
                requirements.append(line)
    return requirements


# Package Metadata
PACKAGE_NAME = "apple_qml"
VERSION = "1.0.0"
DESCRIPTION = "Quantum Machine Learning System für Apfel-Eigenschaftsvorhersage"
LONG_DESCRIPTION = read_file('docs/README.md')
AUTHOR = "QML Development Team"
AUTHOR_EMAIL = "qml-team@example.com"
URL = "https://github.com/username/apple-qml-system"
LICENSE = "MIT"

# Requirements
INSTALL_REQUIRES = read_requirements('requirements.txt')
EXTRAS_REQUIRE = {
    'dev': read_requirements('requirements-dev.txt'),
    'jupyter': [
        'jupyter>=1.0.0',
        'jupyterlab>=4.0.0',
        'ipywidgets>=8.0.0'
    ],
    'visualization': [
        'plotly>=5.15.0',
        'bokeh>=3.2.0'
    ]
}

# Classifiers für PyPI
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Physics',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# Keywords
KEYWORDS = [
    'quantum machine learning',
    'qiskit',
    'quantum computing',
    'parametrized quantum circuits',
    'variational quantum algorithms',
    'machine learning',
    'regression',
    'quantum neural networks'
]

setup(
    # Basic Information
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    
    # Author Information
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    
    # License
    license=LICENSE,
    
    # Package Discovery
    packages=find_packages(include=['src', 'src.*']),
    package_dir={'': '.'},
    
    # Dependencies
    python_requires='>=3.8',
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    
    # Package Data
    include_package_data=True,
    package_data={
        'apple_qml': [
            'configs/*.yaml',
            'data/*.csv',
            'docs/*.md'
        ]
    },
    
    # Entry Points (CLI noch nicht implementiert)
    # entry_points={
    #     'console_scripts': [
    #         'apple-qml-train=src.cli:train_command',
    #         'apple-qml-predict=src.cli:predict_command',
    #         'apple-qml-visualize=src.cli:visualize_command',
    #     ],
    # },
    
    # Classification
    classifiers=CLASSIFIERS,
    keywords=' '.join(KEYWORDS),
    
    # Project URLs
    project_urls={
        'Bug Reports': f'{URL}/issues',
        'Source': URL,
        'Documentation': f'{URL}/docs',
        'Examples': f'{URL}/tree/main/examples',
    },
    
    # Additional Metadata
    zip_safe=False,
    test_suite='tests',
    tests_require=[
        'pytest>=7.4.0',
        'pytest-cov>=4.1.0'
    ],
)