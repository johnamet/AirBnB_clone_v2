#!/usr/bin/python3
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """
    Base class for all models
    """
    id = Column(String(60), nullable=False, primary_key=True, default=str(uuid.uuid4()))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key != '__class__':
                    setattr(self, key, value)
                if 'id' not in kwargs:
                    setattr(self, 'id', str(uuid.uuid4()))
                if 'created_at' not in kwargs:
                    setattr(self, 'created_at', datetime.now())
                if 'updated_at' not in kwargs:
                    setattr(self, 'updated_at', datetime.now())

    def __str__(self):
        """
        Returns a string representation of the instance
        """
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def save(self):
        """
        Saves the instance to the database
        """
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the instance
        """
        result_dict = self.__dict__.copy()
        result_dict['__class__'] = type(self).__name__
        result_dict['created_at'] = self.created_at.isoformat()
        result_dict['updated_at'] = self.updated_at.isoformat()
        result_dict.pop('_sa_instance_state', None)
        return result_dict

    def delete(self):
        """
        Deletes the instance from the database
        """
        from models import storage
        storage.delete(self)
