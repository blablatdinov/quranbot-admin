"""Caching."""

# https://docs.djangoproject.com/en/4.2/topics/cache/
from server.settings.components import config

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{0}:{1}@{2}:{3}/{4}'.format(
            config('REDIS_USER'),
            config('REDIS_PASS'),
            config('REDIS_HOST'),
            config('REDIS_PORT'),
            config('REDIS_DB'),
        ),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
}


# django-axes
# https://django-axes.readthedocs.io/en/latest/4_configuration.html#configuring-caches

AXES_CACHE = 'default'
