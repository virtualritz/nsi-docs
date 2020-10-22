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
import sphinx_rtd_theme
import os

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
    'sphinxcontrib.rsvgconverter',
    'sphinx_tabs.tabs',
    #'sphinxcontrib.inkscapeconverter'
]

# Warning when the Sphinx Tabs extension is used with unknown
# builders (like the dummy builder) - as it doesn't cause errors,
# we can ignore this so we still can treat other warnings as errors.
sphinx_tabs_nowarn = True

if not os.getenv("SPHINX_NO_SEARCH"):
    extensions.append("sphinx_search.extension")

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

source_encoding = "utf-8-sig"

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
#html_css_files = [
#    'theme_overrides.css',
#]

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    "css/custom.css",
]

html_js_files = [
    "js/custom.js",
]

#epub_static_path = ['_static']

#epub_css_files = [
#    'theme_overrides.css',
#]

latex_elements = {
    'papersize': 'a4paper',
}

#    'inputenc': '\\usepackage[utf8x]{inputenc}',
#    'preamble': r'''
#    \usepackage[none]{hyphenat}
#    \usepackage[document]{ragged2e}
#    '''
