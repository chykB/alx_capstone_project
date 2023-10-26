from datetime import datetime
from flask_login import  UserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from connection import session
from app import login_manager

Base = declarative_base()

class User(Base, UserMixin):
    """User Model
    
    Represents a user in the blogging platform.

    Attributes:
        id (int): A unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        image_file (str): The filename of the user's profile image.
        password (str): The hashed password of the user.
        posts (relationship): One-to-Many relationship with Post model.
        comment (relationship): One-to-Many relationship with Comment model.

    Methods:
        __repr__: Returns a string representation of the user.

    """
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
    """Post Model
    
    Represents a blog post in the platform.

    Attributes:
        id (int): A unique identifier for the post.
        title (str): The title of the post.
        date_posted (datetime): The date and time the post was created.
        content (str): The main content of the post.
        description (str): A brief description of the post.
        post_image_file (str): The filename of the post's image.
        user_id (int): The user who authored the post.
        comment (relationship): One-to-Many relationship with Comment model.
        category_id (int): The category to which the post belongs.
        category (relationship): Many-to-One relationship with Category model.

    Methods:
        __repr__: Returns a string representation of the post.

    """
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
    """Category Model
    
    Represents a category to which posts belong.

    Attributes:
        id (int): A unique identifier for the category.
        category_name (str): The name of the category.

    Methods:
        __repr__: Returns a string representation of the category.

    """
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(100))

    def __repr__(self):
        return f"Category('{self.category_name}')"


class Comment(Base):
    """Comment Model
    
    Represents a comment on a blog post.

    Attributes:
        id (int): A unique identifier for the comment.
        content (str): The content of the comment.
        date_posted (datetime): The date and time the comment was created.
        post_id (int): The post to which the comment is associated.
        user_id (int): The user who posted the comment.

    Methods:
        __repr__: Returns a string representation of the comment.

    """
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"



