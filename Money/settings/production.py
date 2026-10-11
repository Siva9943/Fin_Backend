from .base import *  # noqa: F401,F403

DEBUG = False

# Static files are served by WhiteNoise. The non-manifest storage is used so a
# deployment where collectstatic didn't run (no staticfiles.json) can't turn
# every {% static %} lookup — e.g. the admin — into a 500.
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
