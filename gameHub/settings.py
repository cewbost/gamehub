"""
Django settings for gameHub project on Heroku. For more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import dj_database_url
from enum import Enum
#save the secret data in .env and load with config
#for heroku, you can set for the app config variables in heroku sites
#as heroku can not read .env file
from decouple import config

from logging import handlers

from gameHub import logging as be_logging



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

#URL namespace for social auth
SOCIAL_AUTH_URL_NAMESPACE = 'social'

#Third party SMTP configuration
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend',
    cast=str
)

#PAYMENT Configuration
SELLER_ID = 'wsd2017'

PAYMENT_KEY = '77c3d2e61d46cca01d2b5e18c3c6624e'

#Email Account Activation time in Seconds
ACTIVATION_TIME = 3600

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'social_django',
    'widget_tweaks',
    'rest_framework',
    #wsd apps
    'game',
    'accounts',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'gameHub.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
            'debug': DEBUG,
        },
    },
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = '/'


AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
#for view to communicate with the pipeline pick_group
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['user_group',]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'accounts.pipelines.pick_group',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
)

WSGI_APPLICATION = 'gameHub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'].update(dj_database_url.config(conn_max_age=500))

# Logging stuff
LOG_FILE = os.path.join(BASE_DIR, config('LOG_FILE', default='log/logfile.txt'))

filehandler = {
    'level': 'DEBUG',
    'formatter': 'file_formatter',
    'filename': LOG_FILE,
    'class': 'logging.handlers.RotatingFileHandler',
    'mode': 'a',
    'maxBytes': 1048576,
    'backupCount': 10
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(name)s: %(message)s'
        },
        'message_only': {
            'format': '%(message)s'
        },
        'file_formatter': {
            'format': '%(message)s',
            '()': be_logging.SingleLineFormatter,
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'gameHub.logging.ColoredStreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'simple',
            'colors': {
                'DEBUG':    '\033[94m',
                'INFO':     '\033[92m',
                'WARNING':  '\033[93m',
                'ERROR':    '\033[91m',
                'CRITICAL': '\033[95m' + '\033[1m',
            },
        },
        'filehandler': filehandler,
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'filehandler'],
            'propagate': False,
            'level': 'INFO' if DEBUG else 'WARNING'
        },
        'gameHub': {
            'handlers': ['console', 'filehandler'],
            'propagate': False,
            'level': 'DEBUG' if DEBUG else 'WARNING'
        },
        'accounts': {
            'handlers': ['console', 'filehandler'],
            'propagate': False,
            'level': 'DEBUG' if DEBUG else 'WARNING'
        },
        'game': {
            'handlers': ['console', 'filehandler'],
            'propagate': False,
            'level': 'DEBUG' if DEBUG else 'WARNING'
        },
    }
}


REST_FRAMEWORK = {
    'DEFAULT_VERIONING_CLASS': 'rest_framework.version.URLPathVersioning',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(PROJECT_ROOT), "media_cdn")


class ImageSizeEnum(Enum):
    COVER = (1280, 720)
    THUMBNAIL = (500,400)
    PROFILE = (400, 400)