from ..django import BASE_DIR

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(BASE_DIR + '/khoBlog/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'khoBlog.context_processors.context',
                'khoBlog.context_processors.selected_settings'
            ],
            'libraries': {
                'project_tags': 'khoBlog.templatetags.forms',
            }
        },
    },
]
