#!/usr/bin/python3
"""State Module for HBNB project."""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class State(BaseModel):
    """State class."""

    __tablename__ = 'states'

    name = Column(String(128), nullable=False, default='')

    cities = relationship(
        'City',
        backref='state',
        cascade='all, delete, delete-orphan'
    )
