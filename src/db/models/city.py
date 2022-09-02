"""Модуль содержащий модель города.

Classes:
    City
"""
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.dialects.postgresql import UUID

from db.base import Base


class City(Base):
    """Модель города."""

    __tablename__ = 'cities'

    city_id = Column(UUID(), primary_key=True)
    name = Column(String())
