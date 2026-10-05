#!/usr/bin/python3
"""Review module for the HBNB project."""
from sqlalchemy import Column, ForeignKey, String

from models.base_model import BaseModel


class Review(BaseModel):
    """Review class."""

    __tablename__ = 'reviews'

    place_id = Column(
        String(60),
        ForeignKey('places.id'),
        nullable=False,
        default=''
    )
    user_id = Column(
        String(60),
        ForeignKey('users.id'),
        nullable=False,
        default=''
    )
    text = Column(
        String(1024),
        nullable=False,
        default=''
    )
