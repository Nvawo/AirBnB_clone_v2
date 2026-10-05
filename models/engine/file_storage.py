#!/usr/bin/python3
"""Contains the FileStorage class."""

import json

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary of objects."""
        if cls is None:
            return self.__objects

        objects = {}

        for key, obj in self.__objects.items():
            if isinstance(obj, cls):
                objects[key] = obj

        return objects

    def new(self, obj):
        """Adds a new object to the storage dictionary."""
        if obj is not None:
            key = "{}.{}".format(
                obj.__class__.__name__,
                obj.id
            )
            self.__objects[key] = obj

    def save(self):
        """Serializes objects to the JSON file."""
        objects = {}

        for key, obj in self.__objects.items():
            objects[key] = obj.to_dict()

        with open(self.__file_path, "w") as file:
            json.dump(objects, file)

    def reload(self):
        """Deserializes the JSON file."""
        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }

        try:
            with open(self.__file_path, "r") as file:
                objects = json.load(file)

            self.__objects = {}

            for key, value in objects.items():
                class_name = value.get("__class__")

                if class_name in classes:
                    obj = classes[class_name](**value)
                    self.__objects[key] = obj

        except FileNotFoundError:
            pass
