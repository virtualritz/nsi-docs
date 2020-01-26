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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import datetime

# -- Project information -----------------------------------------------------

project = 'NSI'
copyright = '2015–%d, The 3Delight Team. All rights reserved.' % datetime.datetime.today().year
author = 'Olivier Paquet, Aghiles Kheffache, François Colbert, Berj Bannayan'


# -- General configuration ---------------------------------------------------

# ReadTheDocs sets the master doc to 'contents'. We use Sphinx default 'index'
# so wee need to specify an override.
master_doc = 'index'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinxcontrib.rsvgconverter'
    #'sphinxcontrib.inkscapeconverter'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_logo = 'image/nsi_logo_light.svg'

html_theme_options = {
    'canonical_url': 'nsi.readthedocs.io',
    #'analytics_id': 'UA-XXXXXXX-1',  #  Provided by Google in your dashboard
    'logo_only': True,
    'display_version': False,
    'prev_next_buttons_location': 'both',
    'style_external_links': True,
    #'vcs_pageview_mode': '',
    #'style_nav_header_background': 'black',
    # Toc options
    #'collapse_navigation': True,
    #'sticky_navigation': True,
    #'navigation_depth': 4,
    #'includehidden': True,
    #'titles_only': False
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Overrides mainly to make table cell formatting nicer than in the original
# theme.
html_css_files = [
    'theme_overrides.css',
]

#epub_static_path = ['_static']

#epub_css_files = [
#    'theme_overrides.css',
#]
