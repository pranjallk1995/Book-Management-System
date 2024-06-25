""" module to store all application level constants and configuration values """

import os

from enum import Enum

# DATABASE CONNECTION SETTINGS
DATABASE_USER = os.environ.get("POSTGRES_USER")
DATABASE_USER_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DATABASE_NAME = os.environ.get("POSTGRES_DB")
DATABASE_SERVICE = os.environ.get("POSTGRES_SERVICE")

# DATABASE TABLES
class DatabaseTables(Enum):
    """ class to store all tables in database """
    BOOKS = "books"
    REVIEWS = "reviews"
