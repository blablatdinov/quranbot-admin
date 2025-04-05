import environ

env = environ.Env(
    DEBUG=(bool, False),
    TOOLBAR=(bool, False),
)

environ.Env.read_env('.env')
