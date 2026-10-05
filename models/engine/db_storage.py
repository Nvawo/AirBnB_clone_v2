#!/usr/bin/python3
"""Contains the DBStorage class."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """This class manages storage of hbnb models in a MySQL database."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the database engine."""
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                user, password, host, database
            ),
            pool_pre_ping=True
        )

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session."""
        objects = {}

        classes = {
            'User': User,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Place': Place,
            'Review': Review
        }

        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)

            if cls:
                for obj in self.__session.query(cls).all():
                    key = '{}.{}'.format(
                        obj.__class__.__name__, obj.id
                    )
                    objects[key] = obj
        else:
            for model in classes.values():
                for obj in self.__session.query(model).all():
                    key = '{}.{}'.format(
                        obj.__class__.__name__, obj.id
                    )
                    objects[key] = obj

        return objects

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and initialize the database session."""
        Base.metadata.create_all(self.__engine)

        factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )

        self.__session = scoped_session(factory)

    def close(self):
        """Call remove() method on the current database session."""
        self.__session.remove()
