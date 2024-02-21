#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Column, String, Integer, \
    ForeignKey, Float, Table
from sqlalchemy.orm import relationship

from models import type_storage
from models.base_model import BaseModel, Base

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'), nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'), nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    # For DBStorage
    reviews = relationship('Review', backref='place',
                           cascade='all, delete-orphan')

    if type_storage == 'db':
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False)
    else:
        # For FileStorage
        @property
        def reviews(self):
            import models
            from models.review import Review

            return [review for review in
                    models.storage.all(Review).values()
                    if review.place_id == self.id]

        @reviews.setter
        def reviews(self, value):
            self.review = value

        @property
        def amenities(self):
            return self.amenities

        @amenities.setter
        def amenities(self, value):
            from models import Amenity
            if isinstance(value, Amenity):
                self.amenities.append(value.id)
