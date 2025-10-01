from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------------------
# БАЗОВЫЕ НАСТРОЙКИ
# ------------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # apps
    "catalog",
    "blog",
    "users",
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

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "core.wsgi.application"

# ------------------------------------------------------------------------------
# БАЗА ДАННЫХ (оставляю SQLite, как у тебя в проекте)
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / os.getenv("SQLITE_DB_NAME", "db2.sqlite3"),
    }
}

# ------------------------------------------------------------------------------
# ПАРОЛИ / I18N / TZ
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------------------
# СТАТИКА / МЕДИА
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------------------------
# АУТЕНТИФИКАЦИЯ
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = "users.User"
LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "catalog:home"
LOGOUT_REDIRECT_URL = "catalog:home"

# ------------------------------------------------------------------------------
# EMAIL (консоль для разработки)
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@skystore.local"

# ------------------------------------------------------------------------------
# REDIS + CACHE
# ------------------------------------------------------------------------------
# Включение/выключение кеша флажком
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "1") == "1"

# URL Redis (можешь переписать на docker / memurai)
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/1")

if CACHE_ENABLED:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "KEY_PREFIX": "skystore",
            "TIMEOUT": 300,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                # было: "django_redis.serializers.json.JSONSerializer"
                "SERIALIZER": "django_redis.serializers.pickle.PickleSerializer",
            },
        }
    }
else:
    # fallback на локальный кеш, если кеш выключен
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-skystore",
            "TIMEOUT": 0,  # сразу протухает (по сути выключено)
        }
    }