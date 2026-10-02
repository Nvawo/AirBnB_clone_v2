#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone."""
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel(Base):
    """A base class for all hbnb models."""

    __abstract__ = True

    id = Column(String(60), primary_key=True)
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __init__(self, *args, **kwargs):
        """Instantiate a new model."""
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue

                if key in ("created_at", "updated_at"):
                    if isinstance(value, str):
                        value = datetime.strptime(
                            value,
                            "%Y-%m-%dT%H:%M:%S.%f"
                        )

                setattr(self, key, value)

        if not getattr(self, "id", None):
            self.id = str(uuid.uuid4())

        if not getattr(self, "created_at", None):
            self.created_at = datetime.utcnow()

        if not getattr(self, "updated_at", None):
            self.updated_at = datetime.utcnow()

    def __str__(self):
        """Return a string representation of the instance."""
        cls = type(self).__name__
        return "[{}] ({}) {}".format(
            cls,
            self.id,
            self.__dict__
        )

    def save(self):
        """Update updated_at and save the instance."""
        from models import storage

        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance."""
        dictionary = {}

        for key, value in self.__dict__.items():
            if key != "_sa_instance_state":
                dictionary[key] = value

        dictionary["__class__"] = type(self).__name__
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()

        return dictionary

    def delete(self):
        """Delete the current instance from storage."""
        from models import storage

        storage.delete(self)
