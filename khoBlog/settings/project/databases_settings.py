from ..django import BASE_DIR

# https://docs.djangoproject.com/en/stable/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "OPTIONS": {
            "read_default_file": BASE_DIR + "/my.cnf",
            "init_command": "SET sql_mode='STRICT_ALL_TABLES'; SET default_storage_engine=INNODB;",
            "charset": "utf8mb4",
            "use_unicode": True,
        },
        "CONN_MAX_AGE": 60,
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
