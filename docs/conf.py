# Configuration file for the Sphinx documentation builder.
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'beem-sms-python'
copyright = '2025, James Mashaka'
author = 'James Mashaka'

# Get version from the package
try:
    from beem_sms import __version__
    version = __version__
    release = __version__
except ImportError:
    version = '1.0.2'
    release = '1.0.2'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings.
extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The suffix(es) of source filenames.
source_suffix = ['.rst', '.md']

# The master toctree document.
root_doc = 'index'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------

# MyST parser configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False