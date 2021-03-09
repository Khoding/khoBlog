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
    'bootstrap5',
    'bootstrap_datepicker_plus',
    'captcha',

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
    'accounts',
    'shortener',
    'links',
]
