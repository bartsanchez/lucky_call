from .base import *

DEBUG = False
CELERY_TASK_ALWAYS_EAGER = False

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
