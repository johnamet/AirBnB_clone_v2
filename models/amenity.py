#!/usr/bin/python3
""" Amenity Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table
from sqlalchemy.orm import relationship
from models.place import place_amenity

class Amenity(BaseModel, Base):
    """ Amenity class to store amenity information """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)

    # For DBStorage
    place_amenities = relationship("Place", secondary=place_amenity, viewonly=False)

