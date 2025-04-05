from pathlib import Path

from config.splitted_settings.environ import env

BASE_DIR = Path(__file__).resolve().parent.parent

# FIXME: must be replaced
SECRET_KEY = env(
    'SECRET_KEY',
    str,
    default='django-insecure-0hsf(im%p0x)uy_j(ky)4tnfsbi^$sm9(0(ksz@+q7x)gyvye$',
)

DEBUG = env('DEBUG')

ALLOWED_HOSTS = []

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'
