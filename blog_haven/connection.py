from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus



user = 'chikab'
password = 'useraccount82#@'
db = 'blog'
encoded_password = quote_plus(password)
 
path = f'mysql+mysqldb://{user}:{encoded_password}@localhost:3306/{db}'

database = create_engine(path)


Session = sessionmaker(bind=database)
session = Session()





