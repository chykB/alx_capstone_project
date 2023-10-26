from models import Base
from connection import database

# Create the database tables based on the models defined in 'models' module.
# This step is essential to initialize the database structure.
Base.metadata.create_all(bind=database)