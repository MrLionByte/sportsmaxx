"""
Django settings for MaxSports project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from easy_thumbnails.conf import Settings as thumbnail_settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ld#$%ao+(i)+f6nu$sw6-ue5c=3jk7jbh-dxd5nb#$0n__mvhr"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Web apps
    "index_app",
    "Admin_side_app",
    "category_app",
    "product_app",
    "order_app",
    "coupons_app",
    "banner_app",
    "accounts",
    "user_side",
    "cart_app",
    "payment",
    "wallet",
    # Breadcrumbs
    "dynamic_breadcrumbs",
    # rest_framework_app
    "rest_framework",
    # App for All auth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # Social account providers
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.instagram",
    "allauth.socialaccount.providers.twitter",
    "allauth.socialaccount.providers.facebook",
    # crop
    "easy_thumbnails",
    "image_cropping",
    # Visitors
    "visitors",
]

SITE_ID = 3


THUMBNAIL_PROCESSORS = (
    "image_cropping.thumbnail_processors.crop_corners",
) + thumbnail_settings.THUMBNAIL_PROCESSORS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
    #  Vistor count
    "visitors.middleware.VisitorMiddleware",
]

ROOT_URLCONF = "MaxSports.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["template"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # 'index_app.context_processor.py.custom_context',
                "django.template.context_processors.request",
                "dynamic_breadcrumbs.context_processors.breadcrumbs",
            ],
        },
    },
]


WSGI_APPLICATION = "MaxSports.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "maxsport",
        "USER": "postgres",
        "PASSWORD": "0483",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = [
    {
        "social_core.backends.google.GoogleOAuth2",
    },
    {
        "django.contrib.auth.backends.ModelBackend",
    },
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


SOCIALACCOUNT_LOGIN_ON_GET = True


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Email Backend Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


# SMTP Email config
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "example@gmail.com"
EMAIL_HOST_PASSWORD = "add here"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


# All Auth Backend Configuration for social media Authentication

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

LOGIN_URL = "/user_sign_in/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        # 'OAUTH_PKCE_ENABLED': True,
    }
}

# Django Razor Pay
RAZORPAY_API_KEY = "add here"
RAZORPAY_API_SECRET = "add here"
# To Enable Popus in Django or else it will block the payment popup
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"
