from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class User(BaseModel, Base):
    """
    User class for the HBNB project.

    Attributes:
        email (str): The email address of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        places (relationship): Relationship to the Place class, representing
            all places owned by this user.
        reviews (relationship): Relationship to the Review class, representing
            all reviews written by this user.
    """

    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    places = relationship('Place', backref='user',
                          cascade="all, delete-orphan")
    reviews = relationship('Review', backref='user',
                           cascade="all, delete-orphan")
