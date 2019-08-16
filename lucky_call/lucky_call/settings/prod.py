from .base import *

DEBUG = False

CELERY_TASK_ALWAYS_EAGER = False
CELERY_BROKER_URL = 'redis://redis:6379/0'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'db',
        'NAME': 'luckycall',
        'USER': 'fake_db_user',
        'PASSWORD': 'fake_db_password',
    }
}

ALLOWED_HOSTS = ['*']
