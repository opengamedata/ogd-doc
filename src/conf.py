# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path

OGD_CORE_PATH = os.environ.get('OGD_CORE_PATH', '../opengamedata-core/src/')
sys.path.insert(0, str(Path(OGD_CORE_PATH).resolve()))
print(f"Found ogd-core path as {OGD_CORE_PATH}, which resolves to {str(Path(OGD_CORE_PATH).resolve())}")


# -- Project information -----------------------------------------------------

project = 'OpenGameData'
copyright = '2024, Field Day Lab'
author = 'Luke Swanson'
language = 'en'

# The full version, including alpha/beta/rc tags
release = '1.0'


# -- General configuration ---------------------------------------------------

source_parsers = {
    'graphviz': 'sphinx.ext.graphviz',
    'markdown': 'myst_parser.sphinx_'
}

source_suffix = {
    '.rst' : 'restructuredtext',
    '.txt' : 'restructuredtext',
    '.md'  : 'markdown'
    # '.dot' : 'graphviz'
}

exclude_patterns = [
    "util/templates/*",
]

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.graphviz",
    "sphinx.ext.linkcode",
    "sphinx.ext.todo",
    "sphinx_rtd_theme",
    "myst_parser"
]

suppress_warnings = ["myst.header"]

myst_heading_anchors=4
myst_enable_extensions = [
    "amsmath",
    "dollarmath"
]

autodoc_mock_imports = ["config"]

todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_logo = '../assets/extern/images/logos/ogd/OGD-128.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# -- Options for Extensions --------------------------------------------------

def linkcode_resolve(domain, info):
    if domain != 'py':
        return None
    if not info['module']:
        return None
    filename = info['module'].replace('.', '/')
    return f"https://github.com/opengamedata/opengamedata-core/tree/master/{filename}.py"