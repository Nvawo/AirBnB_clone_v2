#!/usr/bin/python3
"""FileStorage module"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

CLASSES = {"BaseModel": BaseModel, "User": User, "State": State,
           "City": City, "Amenity": Amenity, "Place": Place,
           "Review": Review}


class FileStorage:
    """Serialize instances to a JSON file and back"""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return all objects, or only those of class cls"""
        if cls is None:
            return FileStorage.__objects
        if isinstance(cls, str):
            cls = CLASSES.get(cls)
        if cls is None:
            return {}
        return {k: v for k, v in FileStorage.__objects.items()
                if isinstance(v, cls)}

    def new(self, obj):
        """Add obj to __objects"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Write __objects to the JSON file"""
        data = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def reload(self):
        """Load __objects from the JSON file if it exists"""
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        for key, val in data.items():
            FileStorage.__objects[key] = CLASSES[val["__class__"]](**val)

    def delete(self, obj=None):
        """Delete obj from __objects if present"""
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            FileStorage.__objects.pop(key, None)
