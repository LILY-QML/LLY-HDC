import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

project = 'LLY-HDC'
copyright = '2024, Leon Kaiser'
author = 'Leon Kaiser'
release = '3. August 2024'

templates_path = ['_templates']
exclude_patterns = []
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

html_theme = 'alabaster'
html_static_path = ['_static']
