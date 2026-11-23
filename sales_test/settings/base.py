from datetime import timedelta
import os
from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parents[2]


SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[]).split(',')

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default=[]).split(',')

ENABLE_SWAGGER = config('ENABLE_SWAGGER', default=False, cast=bool)

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'health_check',
    'rest_framework_simplejwt.token_blacklist',
    "django_filters",
]

LOCAL_APPS = [
    'apps.catalog',
    'apps.inventory',
    'apps.reports',
    'apps.shipments',
    'apps.sales',
    'apps.authentication',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sales_test.urls"

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

WSGI_APPLICATION = "sales_test.wsgi.application"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('PG_DB', default='myproject_db'),
        'USER': config('PG_USER', default='myproject_user'),
        'PASSWORD': config('PG_PASSWORD', default='strong_password'),
        'HOST': config('PG_HOST', default='127.0.0.1'),
        'PORT': config('PG_PORT', default='5432'),
    }
}


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


LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"

USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# DRF settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    "EXCEPTION_HANDLER": "apps.authentication.exceptions.custom_exception_handler"
}

MEDIA_ROOT = os.path.join(BASE_DIR, config('MEDIA_DIR', default='media/'))
MEDIA_URL = '/media/'

# Security settings    
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Logging settings
LOG_DIR = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    # 1. Четкий формат с датой и метаданными
    'formatters': {
        'production_format': {
            'style': '{',
            'format': '[{asctime}] {levelname} [{name}:{lineno}] {message}',
        },
    },
    
    # 2. Обработчики (Куда шлем логи)
    'handlers': {
        # Ротация основного лога (макс. 10 МБ на файл, храним 5 старых копий)
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django_info.log'),
            'maxBytes': 10 * 1024 * 1024, # 10 Megabytes
            'backupCount': 5,
            'formatter': 'production_format',
            'encoding': 'utf-8',
        },
        # Отдельный файл только для Ошибок (ERROR и CRITICAL)
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django_errors.log'),
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10, # Ошибки важнее, храним больше копий
            'formatter': 'production_format',
            'encoding': 'utf-8',
        },
        # Вывод в консоль (обязателен, если деплоите через Docker / Heroku)
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'production_format',
        },
    },
    
    # 3. Кто отправляет логи
    'loggers': {
        # Главный логгер Django и сторонних приложений
        'django': {
            'handlers': ['file_info', 'file_errors', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        # Логгер для безопасности (Ошибки авторизации, подозрительные запросы)
        'django.security': {
            'handlers': ['file_errors', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}


# SimpleJWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "ON_LOGIN_SUCCESS": "rest_framework_simplejwt.serializers.default_on_login_success",
    "ON_LOGIN_FAILED": "rest_framework_simplejwt.serializers.default_on_login_failed",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "apps.authentication.serializers.CustomTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "apps.authentication.serializers.CustomTokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "apps.authentication.serializers.CustomTokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "apps.authentication.serializers.CustomTokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",

    "CHECK_REVOKE_TOKEN": True,
    "REVOKE_TOKEN_CLAIM": "hash_password",
    "CHECK_USER_IS_ACTIVE": True,
}


SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': "JWT Authorization header. Example: 'Bearer <your_token>'"
        }
    }
}