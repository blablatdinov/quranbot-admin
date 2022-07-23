from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Класс настроек приложения."""

    PORT: int = 8000
    DATABASE_URL: str
    BASE_DIR: Path = Path(__file__).parent

    class Config(object):
        env_file = '.env'


settings = Settings()
