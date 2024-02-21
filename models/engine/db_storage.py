#!/usr/bin/python3
"""
This module defines a storage engine using MySQL database.
"""

from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base


class DBStorage:
    """
    Database storage engine
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the database engine.
        """
        # Retrieve MySQL database credentials from environment variables
        __user = environ['HBNB_MYSQL_USER']
        __password = environ['HBNB_MYSQL_PWD']
        __database = environ['HBNB_MYSQL_DB']
        __host = environ['HBNB_MYSQL_HOST']

        # Create the engine
        self.__engine = create_engine(
            f'mysql+mysqldb://{__user}:{__password}@{__host}/{__database}',
            pool_pre_ping=True
        )

        # Drop all tables if the environment is 'test'
        if environ['HBNB_ENV'] == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries all objects from a specific class or all classes.

        Args:
            cls (class, optional): The class to query objects from.
                                    Defaults to None.

        Returns:
            dict: A dictionary containing queried objects.
        """
        from models.city import City
        from models.state import State
        from models.amenity import Amenity
        from models.place import Place
        from models.user import User

        if cls is not None:
            # Query objects of a specific class
            query = self.__session.query(cls)
            rows = query.all()
            return {f'{row.to_dict()["__class__"]}.\
                    {row.id}': row for row in rows}
        else:
            # Query objects from all tables
            classes = {"City": City, "State": State,
                       "User": User, 'Place': Place,
                       "Amenity": Amenity, }
            all_rows = {}

            for key, cls in classes.items():
                result = self.__session.query(cls)
                rows = result.all()
                all_rows.update({f'{key}.\
                                 {row.id}': row for row in rows})

            return all_rows

    def new(self, obj):
        """
        Adds a new object to the database session.

        Args:
            obj (object): The object to add.
        """
        if obj:
            self.__session.add(obj)

    def save(self):
        """
        Commits changes to the database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the database session.

        Args:
            obj (object, optional): The object to delete. Defaults to None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Reloads the database session.
        """
        # Create all tables
        Base.metadata.create_all(self.__engine)

        # Create a session
        session_factory = sessionmaker(bind=self.__engine)
        Session = scoped_session(session_factory)
        self.__session = Session()
