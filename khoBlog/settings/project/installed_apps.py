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
    'accounts',

    # Packages Apps
    'impostor',
    'markdownx',
    'graphene_django',
    'bootstrap5',
    'bootstrap_datepicker_plus',
    'captcha',
    'storages',
    'robots',
    'taggit',
    'simple_history',
    'rules',
    'widget_tweaks',
    'sitetree',
    'import_export',
    'compressor',
    'django_filters',

    # Django Packages Apps
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
