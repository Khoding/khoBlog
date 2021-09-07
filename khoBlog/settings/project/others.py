from ..django import BASE_DIR
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
ROOT_URLCONF = 'khoBlog.urls'
WSGI_APPLICATION = 'khoBlog.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
BATON = {
    'SITE_HEADER': 'Khodok\'s Blog',
    'SITE_TITLE': 'Khodok\'s Blog',
    'INDEX_TITLE': 'Khodok\'s Blog administration',
    'SUPPORT_HREF': 'mailto:mail@otto.to.it',
    'COPYRIGHT': 'copyright © 2021 <a href="https://www.otto.to.it">Otto srl</a>',  # noqa
    'POWERED_BY': 'Otto srl',
    'CONFIRM_UNSAVED_CHANGES': False,
    'SHOW_MULTIPART_UPLOADING': True,
    'ENABLE_IMAGES_PREVIEW': True,
    'CHANGELIST_FILTERS_IN_MODAL': True,
    'CHANGELIST_FILTERS_ALWAYS_OPEN': False,
    'CHANGELIST_FILTERS_FORM': True,
    'COLLAPSABLE_USER_AREA': False,
    'MENU_ALWAYS_COLLAPSED': False,
    'MESSAGES_TOASTS': ['success'],
    'GRAVATAR_DEFAULT_IMG': 'robohash',
    'CREDENTIALS': '/static/khoBlog/js/khodoks-blog-lmaooo-6148c477f93a.json',
    'VIEW_ID': 'khodoks-blog-lmaooo',
    'LOGIN_SPLASH': '/static/app/bg.jpg',
    'SEARCH_FIELD': {
        'label': 'Search news',
        'url': '/admin/search/',
    },
    'ANALYTICS': {
        'CREDENTIALS': (BASE_DIR + '/credentials.json'),
        'VIEW_ID': '123456789',
    },
    'MENU': (
        {
            'type': 'title',
            'label': 'System',
            'apps': ('auth', 'blog',),
        },
        {
            'type': 'app',
            'name': 'auth',
            'label': 'Authentication',
            'icon': 'fa fa-lock',
            'models': (
                {
                    'name': 'accounts_customuser',
                    'label': 'Users'
                },
                {
                    'name': 'group',
                    'label': 'Groups'
                },
            )
        },
        {
            'type': 'app',
            'name': 'blog',
            'label': 'Blog',
            'icon': 'fas fa-th',
            'models': (
                {
                    'name': 'post',
                    'label': 'Posts'
                },
                {
                    'name': 'category',
                    'label': 'Categories'
                },
            )
        },
        {
            'type': 'title',
            'label': 'Resources',
            'apps': ('filer', ),
        },
        {
            'type': 'app',
            'name': 'filer',
            'label': 'File explorer',
            'icon': 'fa fa-file'
        },
        {
            'type': 'title',
            'label': 'News',
            'apps': ('news', ),
            'default_open': True,
            'children': [
                {
                    'type': 'free',
                    'label': 'Categories',
                    'url': '/admin/news/category/',
                    're': '^/admin/news/category/(\d*)?'
                },
                {
                    'type': 'model',
                    'label': 'News',
                    'name': 'news',
                    'app': 'news'
                },
            ]
        },
        {
            'type': 'title',
            'label': 'Tools',
            'children': [
                {
                    'type': 'free',
                    'label': 'Password generator',
                    'url': 'https://passwordsgenerator.net/',
                    'perms': ('auth.add_user', 'auth.change_user')
                },
                {
                    'type': 'free',
                    'label': 'Google search',
                    'url': 'http://www.google.com'
                },
                # {
                #     'type': 'free',
                #     'label': 'Dalla change form',
                #     'url': '/admin/newschange/3'
                # },
            ]
        },
    ),
}
