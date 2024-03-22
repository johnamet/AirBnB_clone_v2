#!/usr/bin/python3
"""
This module contains the State class
"""


from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import models
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """
    State class for the HBNB project.

    Attributes:
        name (str): The name of the state.
        cities (relationship): Relationship to the City class, representing
            all cities associated with this state.
    """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if models.type_storage == "db":
        # For DBStorage
        cities = relationship("City",
                              backref="state",
                              cascade="all, delete-orphan")
    else:
        # For filestorage
        @property
        def cities(self):
            """
            List the corresponding cities for a state
            """
            from models import City

            all_obj = models.storage.all(City)
            my_cities = [city for _, city
                         in all_obj.items()
                         if city.state_id == self.id]

            return my_cities
