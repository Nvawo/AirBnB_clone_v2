#!/usr/bin/python3
"""DBStorage module"""
from os import getenv
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
    """MySQL storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """Create the engine"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db),
            pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return a dict of objects: <class-name>.<id> -> object"""
        classes = [User, State, City, Amenity, Place, Review]
        if cls is not None:
            if isinstance(cls, str):
                cls = next((c for c in classes if c.__name__ == cls), None)
            classes = [cls] if cls is not None else []
        result = {}
        for c in classes:
            if not hasattr(c, "__table__"):
                continue
            for obj in self.__session.query(c).all():
                result["{}.{}".format(type(obj).__name__, obj.id)] = obj
        return result

    def new(self, obj):
        """Add obj to the current session"""
        self.__session.add(obj)

    def save(self):
        """Commit the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create tables and the session"""
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(factory)

    def close(self):
        """Close the session"""
        self.__session.remove()
