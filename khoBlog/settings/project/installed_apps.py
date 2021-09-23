# Application definition
from ..django import DEBUG

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.redirects',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'django.forms',

    # Accounts
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.discord',
    'allauth.socialaccount.providers.github',
    'accounts',

    # Packages Apps
    'impostor',
    'markdownx',
    'django_editorjs_fields',
    'graphene_django',
    'captcha',
    'storages',
    'robots',
    'taggit',
    'custom_taggit',
    'taggit_selectize',
    'simple_history',
    'rules',
    'widget_tweaks',
    'sitetree',
    'import_export',
    'compressor',
    'django_filters',
    'pinax.referrals',
    'analytical',
    'django_markup',
    'django_activeurl',

    # Django Packages Apps
    'django_comments_xtd',
    'django_comments',
    'comments',

    # APIs Apps
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'khoBlogAPI',
    'learning_resources',

    # Website Settings App
    'settings_app',

    # Apps
    'blog',
    'portfolio',
    'pages',
    'polls',
    'todo',
    'shortener',
    'links',
    'reading_apis_app',
]

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
        "template_profiler_panel",
    ]

EDITORJS_DEFAULT_PLUGINS = (
    '@editorjs/paragraph',
    '@editorjs/image',
    '@editorjs/header',
    '@editorjs/list',
    '@editorjs/checklist',
    '@editorjs/hyperlink',
    '@editorjs/quote',
    '@editorjs/raw',
    '@editorjs/code',
    '@editorjs/inline-code',
    '@editorjs/embed',
    '@editorjs/delimiter',
    '@editorjs/warning',
    '@editorjs/marker',
    '@editorjs/table',
)

EDITORJS_DEFAULT_CONFIG_TOOLS = {
    'Image': {
        'class': 'ImageTool',
        'inlineToolbar': True,
        "config": {"endpoints": {"byFile": "/editorjs/image_upload/"}},
    },
    'Header': {
        'class': 'Header',
        'inlineToolbar': True,
        'config': {
            'placeholder': 'Enter a header',
            'levels': [2, 3, 4],
            'defaultLevel': 2,
        }
    },
    'Checklist': {'class': 'Checklist', 'inlineToolbar': True},
    'Checklist': {'class': 'Checklist', 'inlineToolbar': True},
    'List': {'class': 'List', 'inlineToolbar': True},
    'Quote': {'class': 'Quote', 'inlineToolbar': True},
    'Raw': {'class': 'RawTool'},
    'Code': {'class': 'CodeTool'},
    'InlineCode': {'class': 'InlineCode'},
    'Embed': {'class': 'Embed'},
    'Delimiter': {'class': 'Delimiter'},
    'Warning': {'class': 'Warning', 'inlineToolbar': True},
    'Marker': {'class': 'Marker', 'inlineToolbar': True},
    'Table': {'class': 'Table', 'inlineToolbar': True},
}
