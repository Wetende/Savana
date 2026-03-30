import os
from datetime import timedelta
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name: str, default: list[str]) -> list[str]:
    value = os.getenv(name)
    if not value:
        return default
    return [item.strip() for item in value.split(",") if item.strip()]


DEBUG = env_bool("DJANGO_DEBUG", True)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "local-dev-secret-key-change-me-before-production-2026"
    else:
        raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set when DJANGO_DEBUG is False.")
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", ["127.0.0.1", "localhost", "testserver"])

DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").strip().lower()

if DB_ENGINE == "mysql":
    import pymysql

    pymysql.install_as_MySQLdb()

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME", "coffee"),
            "USER": os.getenv("DB_USER", "root"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "apps.core",
    "apps.users",
    "apps.catalog",
    "apps.blog",
    "apps.sales",
    "apps.orders",
    "apps.payments",
    "apps.reviews",
    "apps.newsletter",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "users.User"

LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

EMAIL_BACKEND = os.getenv(
    "DJANGO_EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@coffee.local")

SESSION_COOKIE_SECURE = env_bool("DJANGO_SESSION_COOKIE_SECURE", not DEBUG)
CSRF_COOKIE_SECURE = env_bool("DJANGO_CSRF_COOKIE_SECURE", not DEBUG)
SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", not DEBUG)
SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_SECURE_HSTS_SECONDS", "0" if DEBUG else "3600"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", not DEBUG)
SECURE_HSTS_PRELOAD = env_bool("DJANGO_SECURE_HSTS_PRELOAD", False)
SECURE_REFERRER_POLICY = os.getenv("DJANGO_SECURE_REFERRER_POLICY", "same-origin")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "200/hour",
        "user": "1000/hour",
        "auth": "30/hour",
        "lead-capture": "60/hour",
        "guest-quote": "60/hour",
        "webhook": "120/hour",
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
    },
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Coffee Backend API",
    "DESCRIPTION": "Wholesale-first backend API for the Coffee platform.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "ENUM_NAME_OVERRIDES": {
        "PublishStatusEnum": [
            ("draft", "Draft"),
            ("published", "Published"),
        ],
        "InquiryStatusEnum": [
            ("new", "New"),
            ("reviewing", "Reviewing"),
            ("quoted", "Quoted"),
            ("closed", "Closed"),
        ],
        "QuoteStatusEnum": [
            ("draft", "Draft"),
            ("sent", "Sent"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
            ("converted", "Converted"),
            ("expired", "Expired"),
        ],
        "OrderStatusEnum": [
            ("draft", "Draft"),
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("fulfilled", "Fulfilled"),
            ("cancelled", "Cancelled"),
        ],
        "OrderPaymentStatusEnum": [
            ("unpaid", "Unpaid"),
            ("authorized", "Authorized"),
            ("paid", "Paid"),
            ("refunded", "Refunded"),
            ("failed", "Failed"),
        ],
        "PaymentStatusEnum": [
            ("pending", "Pending"),
            ("processing", "Processing"),
            ("succeeded", "Succeeded"),
            ("failed", "Failed"),
            ("cancelled", "Cancelled"),
            ("refunded", "Refunded"),
        ],
        "ReviewStatusEnum": [
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        "NewsletterStatusEnum": [
            ("subscribed", "Subscribed"),
            ("unsubscribed", "Unsubscribed"),
        ],
        "AvailabilityStatusEnum": [
            ("available", "Available"),
            ("limited", "Limited"),
            ("sold_out", "Sold Out"),
            ("inquiry", "Inquiry Required"),
        ],
    },
    "TAGS": [
        {"name": "System", "description": "Health checks, API index, and backend documentation entrypoints."},
        {"name": "Authentication", "description": "Customer registration, token auth, and current-user profile APIs."},
        {"name": "Catalog", "description": "Products, categories, variants, wholesale offers, and inventory."},
        {"name": "Blog", "description": "Blog posts, blog categories, and tags."},
        {"name": "Sales & Quotes", "description": "Wholesale inquiries, quotes, guest quote access, and quote conversion."},
        {"name": "Orders & Shipping", "description": "Customer addresses, orders, fulfillment, and shipping-related order data."},
        {"name": "Payments", "description": "Payments, payment attempts, and payment webhook entrypoints."},
        {"name": "Reviews", "description": "Product review submission, moderation, and public review visibility."},
        {"name": "Newsletter", "description": "Newsletter subscriptions and staff-side subscription management."},
    ],
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
