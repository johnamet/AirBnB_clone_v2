from sqlalchemy import Column, String, ForeignKey

from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """
    Review class for the HBNB project.

    Attributes:
        place_id (str): The ID of the place associated with the review.
        user_id (str): The ID of the user who created the review.
        text (str): The text content of the review.
    """

    __tablename__ = "reviews"
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    text = Column(String(1024), nullable=False)
