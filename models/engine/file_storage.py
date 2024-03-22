#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is not None:
            cls_name = cls.__name__
            return {key: value for key, value in
                    FileStorage.__objects.items() if cls_name in key}
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = obj.__class__.__name__ + '.' + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {key: obj.to_dict() for key,
                    obj in FileStorage.__objects.items()}
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                from models.base_model import BaseModel
                from models.user import User
                from models.place import Place
                from models.state import State
                from models.city import City
                from models.amenity import Amenity
                from models.review import Review

                classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                }
                for key, val in temp.items():
                    print(f"key: {key} value: {val}")
                    class_name = val['__class__']
                    class_instance = classes[class_name]
                    val['__class__'] = class_instance
                    self.__objects[key] = class_instance(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects.
        If obj is None, do nothing.
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            del self.__objects[key]

    def close(self):
        """
        Deserializing the JSON file to objects
        """
        reload()
