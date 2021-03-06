"""
Django settings for calyx.

Calyx is a backend implementation of Saffron ( https://github.com/StudioAquatan/Saffron.git ).
"""

import datetime
import os

import dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env_file = os.path.join(os.path.dirname(BASE_DIR), '.env.dev.local')

if os.path.exists(env_file):
    dotenv.load_dotenv(env_file)

DEBUG = os.getenv('CALYX_DEBUG', 'False').lower() == 'true'

SECRET_KEY = os.getenv('CALYX_SECRET_KEY')

ALLOWED_HOSTS = []

for host in os.getenv('CALYX_ALLOWED_HOSTS', '*').split(','):
    ALLOWED_HOSTS.append(host.strip())

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'corsheaders',
    'djoser',
    'courses',
    'users',
    'drf_yasg',
]

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'calyx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'calyx.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('BULB_DB_NAME'),
        'USER': os.getenv('BULB_DB_USER'),
        'HOST': os.getenv('BULB_DB_HOST'),
        'PASSWORD': os.getenv('BULB_DB_PASSWORD'),
        'PORT': int(os.getenv('BULB_DB_PORT', '3306')),
    }
}

# TODO: 本番環境ではRedisかMemcachedにした方が良い
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

DEFAULT_FROM_EMAIL = os.getenv('CALYX_EMAIL_DEFAULT_FROM', 'example@example.com')
EMAIL_ENABLED = os.getenv('CALYX_EMAIL_ENABLED', 'False').lower() == 'true'

if EMAIL_ENABLED:
    EMAIL_HOST = os.getenv('CALYX_EMAIL_HOST')
    EMAIL_PORT = int(os.getenv('CALYX_EMAIL_PORT'))
    EMAIL_HOST_USER = os.getenv('CALYX_EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('CALYX_EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = os.getenv('CALYX_EMAIL_USE_TLS', 'False').lower() == 'true'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # デバッグ時はコンソールに出力

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/#/{uid}/{token}',
    'ACTIVATION_URL': 'activate/#/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserCreateSerializer',
    },
    'EMAIL': {
        'activation': 'users.email.SaffronActivationEmail',
        'confirmation': 'users.email.SaffronConfirmationEmail',
        'password_reset': 'users.email.SaffronPasswordResetEmail',
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(
        hours=int(os.getenv('CALYX_JWT_EXPIRATION_HOURS', '24'))
    ),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(
        hours=int(os.getenv('CALYX_JWT_REFRESH_EXPIRATION_HOURS', '168'))
    ),
    'AUTH_HEADER_TYPES': ('JWT',),
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

PIN_CODE_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

SWAGGER_SETTINGS = {
    'LOGIN_URL': 'accounts:login',
    'LOGOUT_URL': 'accounts:logout',
    'DEFAULT_MODEL_RENDERING': 'example'
}

CORS_ORIGIN_ALLOW_ALL = os.getenv("CALYX_CORS_ALLOW_ALL", "False").lower() == 'true'

CORS_ORIGIN_WHITELIST = [
    origin.strip() for origin in os.getenv("CALYX_CORS_ORIGIN_WHITELIST", "*").split(",")
]

LANGUAGE_CODE = 'ja-jp'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

STUDENT_EMAIL_DOMAIN = os.getenv('CALYX_STUDENT_EMAIL_DOMAIN', 'edu.kit.ac.jp')

# Site and email template variables
SITE_NAME = os.getenv('SITE_NAME', 'Saffron')
MANAGEMENT_TEAM_NAME = os.getenv('CALYX_MANAGEMENT_TEAM_NAME', 'Saffron')
MANAGEMENT_TEAM_EMAIL = os.getenv('CALYX_MANAGEMENT_TEAM_EMAIL', DEFAULT_FROM_EMAIL)

# domain and protocol of petals
PETALS_DOMAIN = os.getenv('PETALS_DOMAIN', 'localhost')
PETALS_PROTOCOL = os.getenv('PETALS_PROTOCOL', 'http')
