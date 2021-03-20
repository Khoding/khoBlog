from ..django import BASE_DIR
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR + '/db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': BASE_DIR + '/my.cnf',
            'init_command': "SET sql_mode='STRICT_ALL_TABLES'; SET default_storage_engine=INNODB;",
            'charset': 'utf8mb4', 'use_unicode': True,
        },
    }
}
