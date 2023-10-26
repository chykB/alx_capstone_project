from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

"""This module configures the database connection and provides a SQLAlchemy session for the Blogging Platform application.

Attributes:
    user: The username for the database connection.
    password: The password for the database connection.
    db: The name of the database.
    encoded_password: The URL-encoded database password.
    path: The complete database URL.
    database: The SQLAlchemy database engine instance.
    Session: The sessionmaker instance for creating SQLAlchemy sessions.
    session: The active SQLAlchemy session for the application.

"""

user = 'chikab'
password = 'useraccount82#@'
db = 'blog'
encoded_password = quote_plus(password)
 
path = f'mysql+mysqldb://{user}:{encoded_password}@localhost:3306/{db}'
database = create_engine(path)

Session = sessionmaker(bind=database)
session = Session()





