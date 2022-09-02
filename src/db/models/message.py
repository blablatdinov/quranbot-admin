"""Модуль содержащий модель сообщения.

Classes:
    MessageModel
"""
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import JSON, BigInteger, Boolean

from db.base import Base


class MessageModel(Base):  # noqa: WPS110
    """Модель сообщения."""

    __tablename__ = 'messages'

    message_id = Column(BigInteger(), primary_key=True)
    message_json = Column(JSON(), nullable=False)
    is_unknown = Column(Boolean(), nullable=False)
    trigger_message_id = Column(BigInteger(), nullable=True)
