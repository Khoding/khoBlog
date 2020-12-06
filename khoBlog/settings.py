"""
Django settings for khoBlog project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
SITE_ID = 3


ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com',
                 'localhost', '.khodok.xyz']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'django.forms',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.discord',

    # packages apps
    'impostor',
    'markdownx',
    'graphene_django',
    'bootstrap4',
    'bootstrap_datepicker_plus',

    # REST
    'rest_framework',
    'drf_yasg',
    'khoBlogAPI',

    # apps
    'blog',
    'portfolio',
    'pages',
    'polls',
    'todo',
    'users',
    'shortener',
    'links',
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ]
}

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
        'linenums_style': 'inline',
    },
    'pymdownx.snippets': {
        'base_path': BASE_DIR / '_snippets/'
    },
    'pymdownx.tasklist': {
        'custom_checkbox': True
    }
}

AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'khoBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(BASE_DIR / 'khoBlog/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'khoBlog.context_processors.context',
            ],
        },
    },
]

WSGI_APPLICATION = 'khoBlog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/Zurich'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = (BASE_DIR / 'media')

STATIC_ROOT = (BASE_DIR / 'static')

STATICFILES_DIRS = [
    (BASE_DIR / 'khoBlog/static'),
]


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    'impostor.backend.AuthBackend',
)

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

GRAPHENE = {
    'SCHEMA': 'khoBlog.schema.schema',
}
