""" module to store all application level constants and configuration values """

import os

# DATABASE CONNECTION SETTINGS
DATABASE_USER = os.environ.get("POSTGRES_USER")
DATABASE_USER_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DATABASE_NAME = os.environ.get("POSTGRES_DB")
