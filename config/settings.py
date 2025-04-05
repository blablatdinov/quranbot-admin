from split_settings.tools import include

from config.splitted_settings.environ import env

include(
    'splitted_settings/installed_apps.py',
    'splitted_settings/middlewares.py',
    'splitted_settings/environ.py',
    'splitted_settings/boilerplate.py',
    'splitted_settings/db.py',
    'splitted_settings/rest_framework.py',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static' / 'prod'  # noqa: F821

STATICFILES_DIRS = [
    BASE_DIR / 'static' / 'dev',  # noqa: F821
]

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'  # noqa: F821

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

TOOLBAR = env('TOOLBAR')

INTERNAL_IPS = [
    'localhost',
    '127.0.0.1',
]

LOCALE_PATHS = (
    BASE_DIR / 'locale',  # noqa: F821
)
