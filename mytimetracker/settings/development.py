"""
Django settings for mytimetracker project.
"""

from .base import *

SECRET_KEY = "=lf@99!*%6a9hcd5$^6wdnz+d0m@2-c7d5wcxjm$1p(hr3y#q#"

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# MEDIA_ROOT = os.path.join(BASE_DIR, "site_media", "media")
# MEDIA_URL = "/site_media/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "site_media", "static")
STATIC_URL = "/site_media/static/"
