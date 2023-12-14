#!/usr/bin/python3
"""skdhgksjhgfksdhfshdf"""

from sqlalchemy import create_engine
from os import getenv
from sqlalchemy.orm import sessionmaker
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from sqlalchemy.orm import scoped_session
from models.user import User


class DBStorage:
    """"""
    __engine = None
    __session = None

    def __init__(self):
        """"""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, password, host, database),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query objects from the current database session."""
        result = {}
        if cls is None:
            classes_to_query = [State, City, Amenity, Place, Review]
        else:
            classes_to_query = [cls]

        for class_obj in classes_to_query:
            objects = self.__session.query(class_obj)
            for obj in objects:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                result[key] = obj

        return result

    def new(self, obj):
        """"""
        self.__session.add(obj)

    def save(self):
        """"""
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = scoped_session(Session)

    def close(self):
        self.__session.remove()
