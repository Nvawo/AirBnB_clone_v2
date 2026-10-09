#!/usr/bin/python3
"""BaseModel module: common attributes and methods for all models"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()


class BaseModel:
    """Base class for all models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Create an instance, optionally from a kwargs dictionary"""
        for key, value in kwargs.items():
            if key == "__class__":
                continue
            if key in ("created_at", "updated_at") and isinstance(value, str):
                try:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                except ValueError:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            setattr(self, key, value)
        if "id" not in self.__dict__:
            self.id = str(uuid.uuid4())
        if "created_at" not in self.__dict__:
            self.created_at = datetime.utcnow()
        if "updated_at" not in self.__dict__:
            self.updated_at = self.created_at

    def __str__(self):
        """String representation"""
        d = dict(self.__dict__)
        d.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)

    def __repr__(self):
        """Same as __str__"""
        return self.__str__()

    def save(self):
        """Update updated_at, add to storage and commit"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance"""
        d = dict(self.__dict__)
        d["__class__"] = type(self).__name__
        d["created_at"] = self.created_at.isoformat()
        d["updated_at"] = self.updated_at.isoformat()
        d.pop("_sa_instance_state", None)
        return d

    def delete(self):
        """Delete the current instance from storage"""
        models.storage.delete(self)
