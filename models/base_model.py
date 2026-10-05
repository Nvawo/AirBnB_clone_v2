#!/usr/bin/python3
"""This module defines a base class for all hbnb models."""
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel(Base):
    """A base class for all hbnb models."""

    __abstract__ = True

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    def __init__(self, *args, **kwargs):
        """Instantiates a new model."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        if hasattr(self, '__table__'):
            for column in self.__table__.columns:
                if column.name in ('id', 'created_at', 'updated_at'):
                    continue

                default = column.default
                if default is not None and default.is_scalar:
                    setattr(self, column.name, default.arg)

        if kwargs:
            if 'id' in kwargs:
                self.id = kwargs['id']

            if 'created_at' in kwargs:
                value = kwargs['created_at']
                if isinstance(value, str):
                    value = self._parse_datetime(value)
                self.created_at = value

            if 'updated_at' in kwargs:
                value = kwargs['updated_at']
                if isinstance(value, str):
                    value = self._parse_datetime(value)
                self.updated_at = value

            kwargs.pop('__class__', None)

            allowed = {
                'id',
                'created_at',
                'updated_at',
                'email',
                'password',
                'first_name',
                'last_name',
                'name',
                'state_id',
                'city_id',
                'user_id',
                'description',
                'number_rooms',
                'number_bathrooms',
                'max_guest',
                'price_by_night',
                'latitude',
                'longitude',
                'amenity_ids',
                'place_id',
                'text'
            }

            for key, value in kwargs.items():
                if key not in allowed:
                    raise KeyError(key)
                setattr(self, key, value)

        from models import storage

        if storage.__class__.__name__ == 'FileStorage':
            storage.new(self)

    @staticmethod
    def _parse_datetime(value):
        """Convert an ISO formatted string to a datetime object."""
        try:
            return datetime.strptime(
                value,
                '%Y-%m-%dT%H:%M:%S.%f'
            )
        except ValueError:
            return datetime.fromisoformat(value)

    def __str__(self):
        """Returns a string representation of the instance."""
        cls = (str(type(self)).split('.')[-1]).split("'")[0]
        return '[{}] ({}) {}'.format(
            cls,
            self.id,
            self.__dict__
        )

    def save(self):
        """Updates updated_at and saves the object."""
        from models import storage

        self.updated_at = datetime.utcnow()
        storage.save()

    def to_dict(self):
        """Convert the instance into a dictionary."""
        dictionary = self.__dict__.copy()
        dictionary.pop('_sa_instance_state', None)

        dictionary['__class__'] = type(self).__name__

        if isinstance(self.created_at, str):
            self.created_at = self._parse_datetime(self.created_at)

        if isinstance(self.updated_at, str):
            self.updated_at = self._parse_datetime(self.updated_at)

        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        return dictionary

    def delete(self):
        """Delete the current instance from storage."""
        from models import storage

        storage.delete(self)
