"""
Django settings for rpa_orchestrator_project project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import datetime

from django.contrib.messages import constants as message
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
load_dotenv()
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
debug_str_from_dotenv = os.getenv('DEBUG_MODE')
DEBUG = debug_str_from_dotenv == 'True'

allowed_hosts_list = str(os.getenv('ALLOWED_HOSTS_LIST'))
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_list.split(",")]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'crispy_forms',
    'formtools',
    'debug_toolbar',
    'django_celery_results',
    'django_celery_beat',
    'django_filters',
    'channels',
    'corsheaders',
    'orc.apps.OrchestratorConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'rpa_orchestrator_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'rpa_orchestrator_project.ctxprocessor.orchestrator_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'rpa_orchestrator_project.wsgi.application'
ASGI_APPLICATION = 'rpa_orchestrator_project.asgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': str(os.getenv('DB_NAME')),
        'USER': str(os.getenv('DB_USER')),
        'PASSWORD': str(os.getenv('DB_PASSWORD')),
        'HOST': str(os.getenv('DB_HOST')),
        'PORT': str(os.getenv('DB_PORT')),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Custom Django auth settings

AUTH_USER_MODEL = 'orc.User'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(BASE_DIR, 'orc/locale'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'rpa_orchestrator_project/static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Messages built in framework
MESSAGE_TAGS = {
    message.DEBUG: 'alert-secondary',
    message.INFO: 'alert-info',
    message.SUCCESS: 'alert-success',
    message.WARNING: 'alert-warning',
    message.ERROR: 'alert-danger',
}

PROJECT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DATETIME_FORMAT': PROJECT_DATETIME_FORMAT,
}

SIMPLE_JWT = {
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=15),
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=10),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'USER_ID_CLAIM': 'id',
}

INTERNAL_IPS = [
    '127.0.0.1',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REDIS_URL = str(os.getenv('REDIS_URL', 'redis://localhost:6379'))

# celery - redis
# BROKER_URL = 'redis://127.0.0.1:6379/0'
BROKER_URL = [REDIS_URL]    # possible to assign different channel e.g.: redis://localhost:6379/2
BROKER_TRANSPORT = 'redis'

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulercmds:DatabaseScheduler'

# Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
        },
    },
}

# # CORS settings
# CORS_ALLOWED_ORIGINS = [
#     # add allowed origins if dedicated frontend will appear - for future
# ]

CORS_ALLOW_ALL_ORIGINS = True
# AES encryption key
AES_KEY = str(os.getenv('AES_KEY'))
