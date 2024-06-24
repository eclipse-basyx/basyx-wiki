# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'BaSyx Wiki'
copyright = '2024, Eclipse BaSyx™'
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
]

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

# -- Options for EPUB output
epub_show_urls = 'footnote'
