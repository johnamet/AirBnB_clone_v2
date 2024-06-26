#!/usr/bin/python3
"""Initialize the storage engine based on environment variable"""

from os import environ

# Get the type of storage from the environment variable
type_storage = environ['HBNB_TYPE_STORAGE']

# Initialize the storage engine based on the type
if type_storage == 'db':
    from models.engine.db_storage import DBStorage

    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage

    storage = FileStorage()

# Load data from the storage engine
storage.reload()

# Specify which modules to import when using models.*
__all__ = ['BaseModel', 'User', 'State', 'City', 'Amenity', 'Place', 'Review']

# Import all models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
