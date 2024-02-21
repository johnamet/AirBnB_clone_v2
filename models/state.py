from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
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
    
    # For DBStorage
    cities = relationship("City", backref="state", cascade="all, delete-orphan")
