#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone."""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel(Base):
    """A base class for all hbnb models."""

    __abstract__ = True

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model."""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        else:
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.utcnow()
            elif isinstance(kwargs['created_at'], str):
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.utcnow()
            elif isinstance(kwargs['updated_at'], str):
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if '__class__' in kwargs:
                del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance."""
        cls = type(self).__name__
        d = self.__dict__.copy()
        d.pop('_sa_instance_state', None)
        return '[{}] ({}) {}'.format(cls, self.id, d)

    def save(self):
        """Updates updated_at with current time when instance is changed."""
        from models import storage

        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format."""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = type(self).__name__
        if isinstance(self.created_at, datetime):
            dictionary['created_at'] = self.created_at.isoformat()
        if isinstance(self.updated_at, datetime):
            dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop('_sa_instance_state', None)
        return dictionary

    def delete(self):
        """Deletes current instance from storage."""
        from models import storage

        storage.delete(self)
