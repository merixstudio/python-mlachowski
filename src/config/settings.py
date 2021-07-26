import logging
from datetime import timedelta

from django.core.exceptions import ImproperlyConfigured

import environ
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration


env = environ.Env()
root = environ.Path(__file__) - 2

BASE_DIR = root()
DEBUG = env("DEBUG", default=False)
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
HEALTH_CHECK_PATH = env.str("HEALTH_CHECK_PATH", default="health/")
SITE_ID = env("SITE_ID", default=1)
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "config",
)

MIDDLEWARE = (
    "config.middleware.HealthCheckMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

# --- ADMIN ---
LOGIN_REDIRECT_URL = "/admin/"

# --- STATIC FILES ---
STATIC_URL = "/static/"
STATIC_ROOT = env("STATIC_ROOT", default="/project/static")
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

MEDIA_URL = "/media/"
MEDIA_ROOT = env("MEDIA_ROOT", default="/project/media")

AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default=None)
if AWS_STORAGE_BUCKET_NAME is not None:
    INSTALLED_APPS += ("storages",)
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default=None)
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default=None)
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="eu-west-1")
    S3_USE_SIGV4 = True
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_ENDPOINT_URL = f"https://s3.{AWS_S3_REGION_NAME}.amazonaws.com"
    AWS_S3_ADDRESSING_STYLE = env("AWS_S3_ADDRESSING_STYLE", default="virtual")
    AWS_DEFAULT_ACL = env("AWS_DEFAULT_ACL", default=None)

# --- TEMPLATES ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [root("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": (
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
            )
        },
    }
]

# --- REST FRAMEWORK ---
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "NON_FIELD_ERRORS_KEY": "errors",
}


# --- SPECTACULAR ---

SPECTACULAR_SETTINGS = {
    "TITLE": "Project's API",
    "DESCRIPTION": "Project's description",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAuthenticated"],
    "SERVE_AUTHENTICATION": ("rest_framework.authentication.BasicAuthentication",),
}


# --- AUTH ---
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- DEBUG TOOLBAR ---
ENABLE_DEBUG_TOOLBAR = env.bool("ENABLE_DEBUG_TOOLBAR", default=DEBUG)
if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += ("debug_toolbar",)
    MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

    INTERNAL_IPS = ("172.18.0.1", "127.0.0.1", "localhost")
    DEBUG_TOOLBAR_CONFIG = {
        "INTERCEPT_REDIRECTS": False,
        "SHOW_TOOLBAR_CALLBACK": lambda *x: True,
    }

# --- CORS ---
CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ALLOW_ALL", default=False)
CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST", default=[])

# --- TIMEZONE ---
USE_TZ = True
TIME_ZONE = "UTC"

# --- LANGUAGES ---
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = "en-us"

# LANGUAGES = (
#     ("en", _("English")),
#     ("pl", _("Polish")),
# )
LOCALE_PATHS = (root("locale"),)

# --- FILE UPLOAD ---
FILE_UPLOAD_MAX_MEMORY_SIZE = 2_621_440  # i.e. 2.5 MB
FILE_UPLOAD_PERMISSIONS = None
FILE_UPLOAD_DIRECTORY_PERMISSIONS = None

# --- DATABASE ---
DATABASES = {
    "default": env.db(default="postgres://postgres:postgres@postgres:5432/postgres")
}


# --- CELERY ---
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://redis:6379/2")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://redis:6379/3")
CELERY_DEFAULT_QUEUE = env("CELERY_DEFAULT_QUEUE", default="default")
CELERY_BEAT_SCHEDULE = {}

# --- CACHE ---
CACHES = {
    "default": env.cache(
        default="redis://redis:6379/1?client_class=django_redis.client.DefaultClient"
    )
}

# ---- SWAGGER ----
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}
    }
}

# ---- SENTRY ----
SENTRY_AUTO_LOG_STACKS = True
SENTRY_DSN = env("SENTRY_DSN", default=None)

if SENTRY_DSN:
    SENTRY_ENVIRONMENT = env("SENTRY_ENVIRONMENT", default="testing")
    if SENTRY_ENVIRONMENT not in ["testing", "staging", "production"]:
        raise ImproperlyConfigured(
            f'"{SENTRY_ENVIRONMENT}" is not valid sentry environment to use.'
        )

    sentry_logging = LoggingIntegration(
        level=logging.INFO,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR,  # Send errors as events
    )

    sentry_sdk.init(
        environment=SENTRY_ENVIRONMENT,
        dsn=SENTRY_DSN,
        integrations=[sentry_logging, CeleryIntegration(), DjangoIntegration()],
    )

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "root": {"level": "WARNING", "handlers": ["sentry"]},
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            }
        },
        "handlers": {
            "sentry": {
                # To capture more than ERROR, change to WARNING, INFO, etc.
                "level": "ERROR",
                "class": "sentry_sdk.integrations.logging.EventHandler",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django.db.backends": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": False,
            },
            "raven": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
            "sentry.errors": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }
