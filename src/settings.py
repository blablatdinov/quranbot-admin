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
    BASE_DIR: Path = Path(__file__).parent.parent
    LOG_LEVEL: LogLevel = LogLevel.DEBUG
    JWT_SECRET: str
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRES_S: int = 3600
    DEBUG: bool = False
    NATS_HOST: str = 'localhost'
    NATS_PORT: int = 4222
    NATS_TOKEN: str

    class Config(object):
        env_file = '.env'

    @property
    def alembic_db_url(self) -> str:
        """Формирование адреса подключения к БД для алембика.

        :return: str
        """
        uri = str(self.DATABASE_URL)
        if self.DATABASE_URL and self.DATABASE_URL.startswith('postgres://'):
            uri = self.DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        return uri.replace('postgresql', 'postgresql+asyncpg')


settings = Settings()
