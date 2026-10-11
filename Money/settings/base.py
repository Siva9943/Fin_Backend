"""
Base Django settings for the Money (FinTrack) project.
Shared by development.py and production.py.
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from celery.schedules import crontab


# =========================================================
# BASE DIRECTORY & ENVIRONMENT VARIABLES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load variables from the project's .env file
load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    """Read a boolean environment variable."""
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in ("true", "1", "yes", "on")


def env_int(name, default):
    """Read an integer environment variable."""
    value = os.getenv(name)

    if value is None or value.strip() == "":
        return default

    return int(value)


def env_list(name, default=None):
    """Read comma-separated environment variables."""
    value = os.getenv(name)

    if value is None:
        return default or []

    return [item.strip() for item in value.split(",") if item.strip()]


# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be configured in the environment.")

DEBUG = env_bool("DEBUG", False)

ALLOWED_HOSTS = env_list(
    "ALLOWED_HOSTS",
    ["localhost", "127.0.0.1"],
)


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "corsheaders",

    # FinTrack apps
    "apps.accounts",
    "apps.transactions",
    "apps.loans",
    "apps.planning",
    "apps.budgets",
    "apps.analytics",
    "apps.notifications",
    "apps.goals",
    "apps.ai_assistant",
    "apps.reports",
    "apps.investments",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URLS & TEMPLATES
# =========================================================

ROOT_URLCONF = "Money.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Money.wsgi.application"


# =========================================================
# DATABASE
# =========================================================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be configured in the environment.")

import dj_database_url

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# =========================================================
# STATIC & MEDIA FILES
# =========================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    directory
    for directory in [BASE_DIR / "static"]
    if directory.exists()
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# EMAIL
# =========================================================

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)

EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = env_int("EMAIL_PORT", 587)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL", False)
DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    EMAIL_HOST_USER,
)


# =========================================================
# CORS & CSRF
# =========================================================

CORS_ALLOWED_ORIGINS = env_list("CORS_ALLOWED_ORIGINS")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")

CORS_ALLOW_CREDENTIALS = True


# =========================================================
# DJANGO REST FRAMEWORK
# =========================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),
    "PAGE_SIZE": 20,
    "EXCEPTION_HANDLER": "apps.core.exceptions.custom_exception_handler",
}


# =========================================================
# SIMPLE JWT
# =========================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=env_int("ACCESS_TOKEN_LIFETIME", 30)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=env_int("REFRESH_TOKEN_LIFETIME", 7)
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


# =========================================================
# CELERY & REDIS
# =========================================================

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0",
)

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

CELERY_BEAT_SCHEDULE = {
    "send-emi-reminders": {
        "task": "apps.notifications.tasks.send_emi_reminders",
        "schedule": crontab(hour=8, minute=0),
    },
    "detect-overdue-loans": {
        "task": "apps.notifications.tasks.detect_overdue_loans",
        "schedule": crontab(hour=1, minute=0),
    },
    "check-budget-alerts": {
        "task": "apps.notifications.tasks.check_budget_alerts",
        "schedule": crontab(hour=9, minute=0),
    },
    "generate-recurring-transactions": {
        "task": (
            "apps.notifications.tasks."
            "generate_recurring_transactions_for_all_users"
        ),
        "schedule": crontab(hour=0, minute=30),
    },
    "send-monthly-financial-summaries": {
        "task": "apps.notifications.tasks.send_monthly_financial_summaries",
        "schedule": crontab(hour=6, minute=0, day_of_month=1),
    },
    "process-reminders": {
        "task": "apps.notifications.tasks.process_reminders",
        "schedule": crontab(hour=7, minute=0),
    },
    "create-daily-portfolio-snapshot": {
        "task": "apps.investments.tasks.create_daily_portfolio_snapshot",
        "schedule": crontab(hour=2, minute=0),
    },
    "remind-stale-investment-prices": {
        "task": "apps.investments.tasks.remind_stale_investment_prices",
        "schedule": crontab(hour=8, minute=30, day_of_month=1),
    },
}


# =========================================================
# FRONTEND & AI
# =========================================================

FRONTEND_URL = os.getenv("FRONTEND_URL", "")

AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "")
