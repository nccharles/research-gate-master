__author__ = "Sylvie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

from flask_sqlalchemy import SQLAlchemy


class DatabaseProvider:
    def __init__(self):
        self.__db: SQLAlchemy = None

    @property
    def db(self):
        if self.__db is None:
            self.__db = SQLAlchemy()
        return self.__db

    @db.setter
    def db(self, value):
        raise PermissionError(" DB can not be changed")


db_provider = DatabaseProvider()
