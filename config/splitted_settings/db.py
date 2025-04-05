from config.splitted_settings.environ import env

DATABASES = {
    'default': env.db(),
}
