from models import Base
from connection import database

Base.metadata.create_all(bind=database)