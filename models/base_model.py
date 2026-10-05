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
        if not kwargs:
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

            from models import storage
            storage.new(self)
        else:
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())

            if 'created_at' not in kwargs:
                self.created_at = datetime.utcnow()
            elif isinstance(kwargs['created_at'], str):
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'],
                    '%Y-%m-%dT%H:%M:%S.%f'
                )

            if 'updated_at' not in kwargs:
                self.updated_at = datetime.utcnow()
            elif isinstance(kwargs['updated_at'], str):
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'],
                    '%Y-%m-%dT%H:%M:%S.%f'
                )

            if '__class__' in kwargs:
                del kwargs['__class__']

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
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        return dictionary

    def delete(self):
        """Delete the current instance from storage."""
        from models import storage

        storage.delete(self)
