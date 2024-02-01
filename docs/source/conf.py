#!/usr/bin/env python3

"""
Script
------

    conf.py

Description
-----------

    This script is the driver script for configuring the
    `sphinx-build` runtime environment in order to build the
    respective API.

Author(s)
---------

    Henry R. Winterbottom; 29 October 2023

History
-------

    2023-10-29: Henry Winterbottom -- Initial implementation.

"""

# ----


import os
import subprocess
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.join(os.path.abspath("."), "../../sorc"))
sys.path.insert(0, os.path.abspath("../../sorc"))
subprocess.run(
    [
        "git",
        "clone",
        "--recursive",
        "https://github.com/HenryWinterbottom-NOAA/ufs_pyutils.git",
    ],
    check=True,
    text=True,
)
sys.path.insert(0, os.path.join(os.getcwd(), "ufs_pyutils"))
subprocess.run(
    [
        "pip",
        "install",
        "-r",
        os.path.join(os.getcwd(), "ufs_pyutils", "requirements.txt"),
    ]
)
#subprocess.run(['git', 'clone', '--recursive',
#                'https://github.com/HenryWinterbottom-NOAA/ufs_pyutils.git'], check=True, text=True)
#sys.path.insert(0, os.path.join(os.getcwd(), "ufs_pyutils/sorc"))

# ----


def setup(app):
    app.add_css_file("custom.css")  # may also be an URL
    app.add_css_file("theme_overrides.css")  # may also be an URL

# ----


project = "UFS Observation Processing API"
copyright = "2023 Henry R. Winterbottom"
author = "2023 Henry R. Winterbottom"
# release = None

# General configuration
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "numpydoc",
    "sphinx_autodoc_typehints",
    "readthedocs_ext.readthedocs",
]
exclude_patterns = []
source_suffix = ".rst"
master_doc = "index"

# API attributes.
autoapi_dirs = [
    "../../sorc",
]
autoapi_type = "python"
autoapi_ignore = []

# Options for HTML output.
pygments_style = "sphinx"
html_theme = "furo"
html_theme_path = ["_themes"]
html_theme_options = {"body_max_width": "none"}
html_static_path = []
html_context = {}
htmlhelp_basename = "ufs_obs"
