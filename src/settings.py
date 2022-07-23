import enum
from pathlib import Path

from pydantic import BaseSettings


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """Класс настроек приложения."""

    PORT: int = 8000
    DATABASE_URL: str
    BASE_DIR: Path = Path(__file__).parent
    LOG_LEVEL: LogLevel = LogLevel.DEBUG

    class Config(object):
        env_file = '.env'


settings = Settings()
