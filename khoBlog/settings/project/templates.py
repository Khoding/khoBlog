from ..django import BASE_DIR

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [(BASE_DIR + "/khoBlog/templates")],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "khoBlog.context_processors.context",
                "khoBlog.context_processors.selected_settings",
            ],
            "libraries": {
                "project_tags": "khoBlog.templatetags.forms",
                "cards": "khoBlog.templatetags.cards",
                "content_type": "khoBlog.templatetags.content_type",
                "display": "khoBlog.templatetags.display",
            },
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                ),
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.request",)

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"
