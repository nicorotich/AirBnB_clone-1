#!/usr/bin/python3
"""Module for database storage engine"""


import models
import os
from models import base_model
from sqlalchemy import create_engine
from sqlalchemy import orm


class DBStorage:
    """Store data model objects in a database"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the database storage with environment inputs"""

        dbName = os.getenv('HBNB_MYSQL_DB', '')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.getenv('HBNB_MYSQL_USER', ''),
                os.getenv('HBNB_MYSQL_PWD', ''),
                os.getenv('HBNB_MYSQL_HOST', ''),
                dbName
            ),
            pool_pre_ping=True
        )
        if os.getenv('HBNB_ENV', '') == 'test':
            models.base_model.Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return a collection of objects"""

        mylist = []
        newdict = {}
        if cls is not None:
            obj = eval(cls)
            mylist = self.__session.query(obj).all()
            for item in mylist:
                key = item.__class__.__name__ + "." + item.id
                newdict[key] = item
        else:
            for obj in ["State", "City", "User",
                        "Place", "Review", "Amenity"]:
                obj = eval(obj)
                mylist = self.__session.query(obj).all()
                for item in mylist:
                    key = item.__class__.__name__ + "." + item.id
                    newdict[key] = item
        return (newdict)

    def delete(self, obj=None):
        """Delete obj from the database"""
        if obj is not None:
            self.__session.delete(obj)

    def new(self, obj):
        """Save a new object to the database"""
        self.__session.add(obj)

    def reload(self):
        """Open a new session"""

        base_model.Base.metadata.create_all(self.__engine)
        session_maker = orm.session.sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = orm.scoped_session(session_maker)
        self.__session = Session()

    def save(self):
        """commit all current pending changes to the database"""
        self.__session.commit()
