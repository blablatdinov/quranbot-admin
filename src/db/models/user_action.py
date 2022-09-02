"""Модуль содержащий модель действий пользователей.

Classes:
    UserAction
"""
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from db.base import Base


class UserAction(Base):
    """Модель действий пользователей."""

    __tablename__ = 'user_actions'

    user_action_id = Column(UUID(), primary_key=True)
    date_time = Column(DateTime(), nullable=False)
    action = Column(String(), nullable=False)
    user_id = Column(Integer(), ForeignKey('users.chat_id'))
