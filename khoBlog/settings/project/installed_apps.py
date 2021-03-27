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

    # APIs Apps
    'rest_framework',
    'drf_yasg',
    'khoBlogAPI',

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
]
