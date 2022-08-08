"""Модуль с настройками приложения.

Classes:
    LogLevel: перечисление уровней логгирования
    Settings: конфигурация приложения

Misc variables:
    settings: объект для использования настроек в коде
"""
import enum
from pathlib import Path

from pydantic import BaseSettings, PostgresDsn, RedisDsn


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = 'NOTSET'
    DEBUG = 'DEBUG'
    INFO = 'INFO'  # noqa: WPS110
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    FATAL = 'FATAL'


class Settings(BaseSettings):
    """Класс настроек приложения."""

    PORT: int = 8000
    DATABASE_URL: PostgresDsn
    REDIS_DSN: RedisDsn
    BASE_DIR: Path = Path(__file__).parent
    LOG_LEVEL: LogLevel = LogLevel.DEBUG
    JWT_SECRET: str
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRES_S: int = 3600

    class Config(object):
        env_file = '.env'


settings = Settings()
