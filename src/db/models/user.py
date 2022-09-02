"""Модуль содержащий модель пользователя.

Classes:
    User
"""
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, Integer, String

from db.base import Base


class User(Base):
    """Модель пользователя."""

    __tablename__ = 'users'

    chat_id = Column(BigInteger(), primary_key=True, autoincrement=False)
    username = Column(String())
    password_hash = Column(String())
    is_active = Column(Boolean(), nullable=False)
    comment = Column(String())
    day = Column(Integer())
    city_id = Column(String(), ForeignKey('cities.city_id'))
    referrer_id = Column(Integer(), ForeignKey('users.chat_id'))
    legacy_id = Column(Integer(), nullable=True)
