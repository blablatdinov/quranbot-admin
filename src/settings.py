from pydantic import BaseSettings


class Settings(BaseSettings):
    """Класс настроек приложения."""

    PORT: int = 8000

    class Config(object):
        env_file = '.env'


settings = Settings()
