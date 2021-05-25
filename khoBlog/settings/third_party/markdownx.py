from datetime import datetime

from ..django import BASE_DIR

# Markdown extensions
MARKDOWNX_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.sane_lists',
    'markdown.extensions.nl2br',
    'markdown.extensions.admonition',
    'markdown.extensions.codehilite',
    'markdown.extensions.legacy_attrs',
    'markdown.extensions.legacy_em',
    'markdown.extensions.meta',
    'markdown.extensions.smarty',
    'markdown.extensions.toc',
    'markdown.extensions.wikilinks',
    'pymdownx.arithmatex',
    'pymdownx.b64',
    'pymdownx.caret',
    'pymdownx.critic',
    'pymdownx.details',
    'pymdownx.saneheaders',
    'pymdownx.emoji',
    'pymdownx.escapeall',
    'pymdownx.extra',
    'pymdownx.highlight',
    'pymdownx.inlinehilite',
    'pymdownx.keys',
    'pymdownx.magiclink',
    'pymdownx.pathconverter',
    'pymdownx.progressbar',
    'pymdownx.smartsymbols',
    'pymdownx.snippets',
    'pymdownx.striphtml',
    'pymdownx.tabbed',
    'pymdownx.tasklist',
    'pymdownx.tilde',
    'pyembed.markdown',
]

MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = {
    'pymdownx.highlight': {
        'guess_lang': True,
        'linenums': True,
        'linenums_style': 'table',
    },
    'pymdownx.snippets': {
        'base_path': BASE_DIR + '/_snippets/'
    },
    'pymdownx.tasklist': {
        'custom_checkbox': True
    },
    'pymdownx.critic': {
        'mode': 'view'
    },
    'pymdownx.magiclink': {
        'repo_url_shortener': True,
        'social_url_shortener': True,
        'repo_url_shorthand': True,
        'social_url_shorthand': True,
        'user': 'Khoding',
        'repo': 'khoBlog',
        'normalize_issue_symbols': True
    },
}

MARKDOWNX_MEDIA_PATH = datetime.now().strftime('images/markdownx/%Y/%m/%d')
MARKDOWNX_UPLOAD_URLS_PATH = '/markdownx/upload/'
MARKDOWNX_UPLOAD_CONTENT_TYPES = [
    'image/jpeg', 'image/png', 'image/svg+xml', 'image/gif']
