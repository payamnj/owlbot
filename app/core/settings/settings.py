"""
Django settings for owlbot project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sentry_sdk
from google.oauth2 import service_account

from .utils import get_env_variable

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

sentry_sdk.init(
    "https://{}@sentry.io/{}".format(os.getenv('SENTRY_PUBLIC_KEY'), os.getenv('SENTRY_PROJECT_ID')))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'app.core',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app.dictionary',
    'app.local_scripts',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    'easy_thumbnails',
    'image_cropping',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

from easy_thumbnails.conf import Settings as thumbnail_settings


THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

ROOT_URLCONF = 'app.core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': '',
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

DEFAULT_FILE_STORAGE = 'app.dictionary.gc-storage.OwlBotGCStorage'
THUMBNAIL_DEFAULT_STORAGE = 'app.dictionary.gc-storage.OwlBotGCStorage'
GS_BUCKET_NAME = 'media.owlbot.info'
GS_PROJECT_ID = os.getenv('PROJECT_ID', '')
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    '/secrets/service-account.json')
GS_CUSTOM_DOMAIN = 'https://media.owlbot.info'
STATIC_URL = '/static/'
MEDIA_URL = 'https://media.owlbot.info/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
