#

# Third Party packages for FastApi
import databases  # Databases gives you simple asyncio support for a range of databases.
import sqlalchemy  # A powerful and popular Object-Relational Mapping (ORM) library that supports multiple database backends, including PostgreSQL, MySQL, SQLite, and more.
from decouple import config

#! Postgress Settings
POSTGRES_HOST = config("POSTGRES_HOST")
POSTGRES_DB = config("POSTGRES_DB")
POSTGRES_USER = config("POSTGRES_USER")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")
POSTGRES_PORT = config("POSTGRES_PORT", 5432)

#! Database Url
DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(
    POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
)

#! Create database object from Database class
database = databases.Database(DATABASE_URL)


#! Sqlalchemy and Tables
metadata = sqlalchemy.MetaData()
