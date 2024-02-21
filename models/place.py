from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship

from models import type_storage

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'), nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'), nullable=False))


class Place(BaseModel, Base):
    """
    Place class for the HBNB project.

    Attributes:
        city_id (str): The ID of the city where the place is located.
        user_id (str): The ID of the user who owns the place.
        name (str): The name of the place.
        description (str): The description of the place.
        number_rooms (int): The number of rooms in the place.
        number_bathrooms (int): The number of bathrooms in the place.
        max_guest (int): The maximum number of guests the place can accommodate.
        price_by_night (int): The price per night for the place.
        latitude (float): The latitude coordinate of the place.
        longitude (float): The longitude coordinate of the place.
    """

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
        amenities = relationship('Amenity', secondary=place_amenity, viewonly=False)
    else:
        # For FileStorage
        @property
        def reviews(self):
            """Getter attribute to retrieve reviews associated with the place."""
            import models
            from models.review import Review

            return [review for review in models.storage.all(Review).values() if review.place_id == self.id]

        @reviews.setter
        def reviews(self, value):
            """Setter attribute to set reviews associated with the place."""
            self.review = value

        @property
        def amenities(self):
            """Getter attribute to retrieve amenities associated with the place."""
            return self.amenities

        @amenities.setter
        def amenities(self, value):
            """Setter attribute to set amenities associated with the place."""
            from models import Amenity
            if isinstance(value, Amenity):
                self.amenities.append(value.id)
