"""
Django settings for project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

from decouple import config, Csv
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# ============================================= APPLICATION SECURITY ===================================================
# SECURITY WARNING: keep the secret key used in production secret!
DEBUG = config("DEBUG", cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
SECRET_KEY = config("SECRET_KEY", 'django-insecure-bh)8k0mqj%i5mq9q#t@7xv&@bz5hac+(1b-*4x($hz45mq13ku')

# =============================================== DJANGO APPS ==========================================================
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.admindocs',

    # postgres
    'django.contrib.postgres',

    # Healthcheck
    'health_check',  # required
    'health_check.db',  # stock Django health checkers
    'health_check.cache',
    # 'health_check.storage',
    'health_check.contrib.migrations',
    'health_check.contrib.celery',  # requires celery
    'health_check.contrib.celery_ping',  # requires celery
    'health_check.contrib.psutil',  # disk and memory utilization; requires psutil
    # 'health_check.contrib.s3boto3_storage',     # requires boto3 and S3BotoStorage backend
    'health_check.contrib.redis',  # requires Redis broker

    # Celery
    'django_celery_results',

    # Django extensions
    'django_extensions',

    # Rest framework
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'rest_framework_swagger',

    # Apps
    'apps.stock',
]

if DEBUG is True:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

# ============================================== WEB APPLICATION =======================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
]

if DEBUG is True:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

ROOT_URLCONF = 'project.urls'

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
            'libraries': {  # Adding this section should work around the issue.
                'staticfiles': 'django.templatetags.static',
            },
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CORS_ORIGIN_ALLOW_ALL = config('CORS_ORIGIN_ALLOW_ALL', cast=bool, default=True)
if CORS_ORIGIN_ALLOW_ALL is False:
    CORS_ORIGIN_WHITELIST = config('CORS_ORIGIN_WHITELIST', cast=lambda v: [s.strip() for s in v.split(',')])

# ================================================== SECURITY ==========================================================
# Increase value according to doc: https://docs.djangoproject.com/en/4.1/ref/middleware/#http-strict-transport-security
# Once you confirm that all assets are served securely on your site (i.e. HSTS didn’t break anything), it’s a good idea
# to increase this value so that infrequent visitors will be protected (31536000 seconds, i.e. 1 year, is common).
SECURE_HSTS_SECONDS = 0 if DEBUG else 3600

SECURE_HSTS_INCLUDE_SUBDOMAINS = DEBUG is False
SECURE_SSL_REDIRECT = DEBUG is False
SESSION_COOKIE_SECURE = DEBUG is False
CSRF_COOKIE_SECURE = DEBUG is False
SECURE_HSTS_PRELOAD = DEBUG is False

# ================================================= DATABASES ==========================================================
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": config("DB_DEFAULT_HOST", "postgres"),
        "NAME": config("DB_DEFAULT_NAME", "db"),
        "USER": config("DB_DEFAULT_USER", "postgres"),
        "PASSWORD": config("DB_DEFAULT_PWD", "postgres"),
        "PORT": config("DB_DEFAULT_PORT", cast=int, default=5432),
        "ATOMIC_REQUESTS": True,
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================== AUTH SECURITY ========================================================
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# ========================================= INTERNATIONALIZATION / DATETIME ============================================
# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGES = (
    ('en-us', _('English (US)')),
    ('pt-br', _('Português (Brasil)')),
)

LANGUAGE_CODE = config('LANGUAGE_CODE', 'en-us')
TIME_ZONE = config('TIME_ZONE', 'UTC')
USE_I18N = config('USE_I18N', cast=bool, default=False)
USE_L10N = config('USE_L10N', cast=bool, default=False)
USE_TZ = config('USE_TZ', cast=bool, default=False)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(BASE_DIR, 'core', 'locale'),
    os.path.join(BASE_DIR, 'apps', 'stock', 'locale'),
]

# ===================================================== FIXTURES / SEEDS ===============================================
FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'project', 'fixtures'),
]

# ======================================================== HEALTHCHECK =================================================
HEALTH_CHECK = {
    'DISK_USAGE_MAX': 90,  # percent
    'MEMORY_MIN': 100,  # in MB
}

# =========================================================== BROKER ===================================================
REDIS_SSL = config('REDIS_SSL', cast=bool, default=False)
REDIS_HOST = config('REDIS_HOST', 'redis')
REDIS_USERNAME = config('REDIS_USERNAME', default='')
REDIS_PORT = config('REDIS_PORT', cast=int, default=6379)

BROKER_REDIS_BASE_URL = 'rediss' if REDIS_SSL else 'redis'
BROKER_REDIS_BASE_URL += f"://{REDIS_USERNAME + '@' if REDIS_USERNAME else ''}"
BROKER_REDIS_BASE_URL += f"{REDIS_HOST}:{REDIS_PORT}"
BROKER_REDIS_BASE_URL += "/{}"

if REDIS_SSL is True:
    BROKER_REDIS_BASE_URL += '?ssl_cert_reqs=required'

# DB 0 will be used for cache
REDIS_URL = BROKER_REDIS_BASE_URL.format(0)  # Redis - Channel 0
# ============================================================ CACHE ===================================================
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        },
        'KEY_PREFIX': 'django_orm'
    }
}

# =========================================================== CELERY ===================================================
CELERY_BROKER_URL = BROKER_REDIS_BASE_URL.format(1)  # Redis - Channel 1

# Celery Configuration Options
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# Celery results configuration
CELERY_RESULT_BACKEND = BROKER_REDIS_BASE_URL.format(2)  # Redis - Channel 2

# =========================================================== CELERY ===================================================
GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}

# ======================================================= REST FRAMEWORK ===============================================
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': [
    #    'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50
}

# ======================================================== E-MAIL ==================================================== #
EMAIL_BACKEND = config('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', 'mailhog')
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=1025)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=False)
