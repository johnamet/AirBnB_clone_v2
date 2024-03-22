from sqlalchemy import Column, String, ForeignKey

from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """
    City class for the HBNB project.

    Attributes:
        name (str): The name of the city.
        state_id (str): The ID of the state to which the city belongs.
    """

    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
