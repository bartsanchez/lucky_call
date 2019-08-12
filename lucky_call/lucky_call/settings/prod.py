from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'db',
        'NAME': 'luckycall',
        'USER': 'fake_db_user',
        'PASSWORD': 'fake_db_password',
    }
}
