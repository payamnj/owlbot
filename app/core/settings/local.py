from .settings import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1223'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
THUMBNAIL_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'owlbot',
        'USER': 'payam',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}
