"""
Django settings for SR_proj project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from kombu import Queue
import ssl
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9-an_5laz%@j-@pi5qmah255n9%mjj+j5bf1zm56%$a#1r4w@%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'helloapp',
    'django_celery_results'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SR_proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'SR_proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/


STATIC_URL = '/static/'

# CELERY SETTINGS SECTION
BROKER_URL = [""]

#BROKER_LOGIN_METHOD = "EXTERNAL"
BROKER_USE_SSL = {
	'keyfile': '/home/aniket/keys-client/key.pem',
	'certfile': '/home/aniket/keys-client/cert.pem',
	'ca_certs': '/home/aniket/keys-client/cacert.pem',
	'cert_reqs': ssl.CERT_REQUIRED
}

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'
# DEFAULT_QUEUE = "celery"
# CELERY_ADD_QUEUE = "addq"
# CELERY_MUL_QUEUE = "mulq"

CELERY_QUEUES = (
	Queue('default', routing_key='default'),
	Queue('addq', routing_key='addq'),
	Queue('mulq', routing_key='mulq'),
)

CELERY_ROUTES = (
	{'helloapp.tasks.add': {'queue': 'addq'}},
	{'helloapp.tasks.mul': {'queue': 'mulq'}},
)

# SECURITY_KEY = '/etc/rmq-ssl/key.pem'
# SECURITY_CERTIFICATE ='/etc/rmq-ssl/cert.pem'
# SECURITY_CERT_STORE ='/etc/rmq-ssl/cacert.pem'

# CELERY_RESULT_BACKEND = 'django-db'

# CELERY_RESULT_BACKEND = 'django-cache'
