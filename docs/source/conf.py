# Configuration file for the Sphinx documentation builder.

import os

# Define the canonical URL if you are using a custom domain on Read the Docs
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")

# Tell Jinja2 templates the build is running on Read the Docs
if os.environ.get("READTHEDOCS", "") == "True":
    if "html_context" not in globals():
        html_context = {}
    html_context["READTHEDOCS"] = True

# -- Project information

project = 'BaSyx Wiki'
copyright = '2025, Eclipse BaSyx™'
author = 'Eclipse BaSyx™'

release = '2.0'
version = '2.0.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'myst_parser',
    'sphinx_copybutton',
    'sphinxcontrib.plantuml',
    'sphinxcontrib.mermaid',
]

# Make Sphinx parse .md files
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Enable fenced directives like ```{include} ... ```
myst_enable_extensions = [
    "colon_fence",
    "attrs_block",
    "linkify",
    "deflist",
    "attrs",
    "dollarmath",
    "amsmath",
]

# Configure MyST to recognize diagram directives
myst_fence_as_directive = ["mermaid", "uml"]

# PlantUML configuration
# Use PlantUML server (works without local Java/PlantUML installation)
plantuml = 'http://www.plantuml.com/plantuml'
plantuml_output_format = 'svg'

# Additional PlantUML options
plantuml_latex_output_format = 'pdf'

# PlantUML directive aliases
plantuml_syntax_error_image = True

# Configure Mermaid for better dark mode support
mermaid_config = {
    "theme": "base",
    "themeVariables": {
        "primaryColor": "#ffffff",
        "primaryTextColor": "#000000",
        "primaryBorderColor": "#444444",
        "lineColor": "#666666",
        "secondaryColor": "#f0f0f0",
        "tertiaryColor": "#e8e8e8",
        "background": "#ffffff",
        "mainBkg": "#ffffff",
        "secondBkg": "#f5f5f5",
        "tertiaryBkg": "#eeeeee",
        "nodeBkg": "#ffffff",
        "nodeBorder": "#cccccc",
        "clusterBkg": "#f9f9f9",
        "clusterBorder": "#dddddd",
        "edgeLabelBackground": "#ffffff",
        "actorBorder": "#cccccc",
        "actorBkg": "#ffffff",
        "actorTextColor": "#000000",
        "actorLineColor": "#666666",
        "signalColor": "#333333",
        "signalTextColor": "#333333",
        "labelBoxBkgColor": "#ffffff",
        "labelBoxBorderColor": "#cccccc",
        "labelTextColor": "#000000",
        "loopTextColor": "#000000",
        "noteBorderColor": "#cccccc",
        "noteBkgColor": "#ffffcc",
        "noteTextColor": "#000000"
    }
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_book_theme'

html_theme_options = {
    "repository_url": "https://github.com/eclipse-basyx/basyx-wiki",
    "use_repository_button": True,
    "use_sidenodes": True,

    "icon_links": [
        {
            "name": "Eclipse BaSyx Open Hour",
            "url": "https://www.iese.fraunhofer.de/en/customers_industries/digitalisierung-produktion/industrie40/basyx_open_hour.html",
            "icon": "_static/logo/favicon-32x32.png",
            "type": "local",
        },
        {
            "name": "GitHub",
            "url": "https://github.com/eclipse-basyx",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "BaSyx Dev Mail",
            "url": "mailto:basyx-dev@eclipse.org",
            "icon": "fa fa-envelope",
        },
        {
            "name": "BaSyx Documentation",
            "url": "https://basyx-wiki.readthedocs.io/",
            "icon": "https://img.shields.io/readthedocs/basyx-wiki",
            "type": "url",
        },
        {
            "name": "Docker",
            "url": "https://hub.docker.com/u/eclipsebasyx",
            "icon": "https://img.shields.io/docker/pulls/eclipsebasyx/aas-server",
            "type": "url",
        },
    ],
}

html_logo = "_static/logo/basyx_logo.png"

html_title = "Eclipse BaSyx™"

html_favicon = "_static/logo/favicon-32x32.ico"

html_css_files = [
    'css/custom.css',
]

html_static_path = ['_static']

# -- Options for EPUB output
epub_show_urls = 'footnote'
