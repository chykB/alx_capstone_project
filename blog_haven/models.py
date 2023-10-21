from datetime import datetime
from flask_login import  UserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from connection import session
from route import login_manager



Base = declarative_base()





class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    image_file = Column(String(20), nullable=False, default='default.jpg')
    password = Column(String(60), nullable=False)
    posts = relationship('Post', backref='author', lazy=True)
    comment = relationship('Comment', backref='author', lazy=True)
    


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)
    content = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    post_image_file = Column(String(20), nullable=False, default='default_image.jpg')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False) 
    comment = relationship('Comment', backref='post', lazy=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category', backref='posts')
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.description}', '{self.post_image_file}')"



class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(100))

    def __repr__(self):
        return f"Category('{self.category_name}')"


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"



