#!/usr/bin/python3
"""Amenity Module for HBNB project."""
from sqlalchemy import Column, String

from models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class."""

    __tablename__ = 'amenities'

    name = Column(
        String(128),
        nullable=False,
        default=''
    )
