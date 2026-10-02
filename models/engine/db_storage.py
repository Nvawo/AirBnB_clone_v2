#!/usr/bin/python3
"""Contains the DBStorage class."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review


classes = {
    "State": State,
    "City": City,
    "User": User,
    "Place": Place,
    "Amenity": Amenity,
    "Review": Review,
}


class DBStorage:
    """Interacts with the MySQL database."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the database engine."""
        user = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        database = os.getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                user,
                password,
                host,
                database
            ),
            pool_pre_ping=True
        )

        if os.getenv("HBNB_ENV") == "test":
            BaseModel.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session."""
        objects = {}

        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)

            if cls:
                for obj in self.__session.query(cls).all():
                    key = "{}.{}".format(
                        type(obj).__name__,
                        obj.id
                    )
                    objects[key] = obj
        else:
            for model in classes.values():
                for obj in self.__session.query(model).all():
                    key = "{}.{}".format(
                        type(obj).__name__,
                        obj.id
                    )
                    objects[key] = obj

        return objects

    def new(self, obj):
        """Add an object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the database."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload objects from the database."""
        BaseModel.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        self.__session = scoped_session(session_factory)

    def close(self):
        """Call remove() on the current SQLAlchemy session."""
        self.__session.remove()
