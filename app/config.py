""" module to store all application level constants and configuration values """

import os

from enum import Enum

# DATABASE CONNECTION SETTINGS
DATABASE_USER = os.environ.get("POSTGRES_USER")
DATABASE_USER_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DATABASE_NAME = os.environ.get("POSTGRES_DB")
DATABASE_SERVICE = os.environ.get("POSTGRES_SERVICE")

# DATABASE CONFIGURATION SETTINGS
class DatabaseTables(Enum):
    """ class to store all tables in database """
    BOOKS = "books"
    REVIEWS = "reviews"

class Genres(Enum):
    """ class to store all the valid genres """
    SPORTS = "Sports"
    SCIENCE = "Science"
    ROMANCE = "Romance"
    DRAMA = "Drama"
    SCIFI = "Sci-Fi"
    COMEDY = "Comedy"
    HORROR = "Horror"
    ADVENTURE = "Adventure"
    FANTASY = "Fantasy"
    AUTOBIOGRAPHY = "Auto-biography"
    BIOGRAPHY = "BIOGRAPHY"
    CRIME = "Crime"

class Ratings(Enum):
    """ class to store all valid ratings """
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

class Books(Enum):
    """ class to store books table schema """
    ID ="id"
    TITLE = "title"
    AUTHOR = "author"
    GENRE = "genre"
    YEAR = "year_published"
    SUMMARY = "summary"

class Reviews(Enum):
    """ class to store reviews table schema """
    ID = "id"
    BOOK_ID = "book_id"
    USER_ID = "user_id"
    REVIEW = "review_text"
    RATING = "rating"

BOOKS_COLUMNS = ["ID", "Title", "Author", "Genre", "Year", "Summary"]
REVIEWS_COLUMNS = ["ID", "Book ID", "User ID", "Review", "Rating"]

MAX_SUMMARY_SIZE = 5000

# USER CREDENTIALS
USER_ID = "100"
