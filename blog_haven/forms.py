from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User, Post, Category
from connection import session
from flask_ckeditor import CKEditorField #subject to change

# Registration Form for new users
class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', 
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('REGISTER')

    # Custom validation to check if the provided username already exists
    def validate_username(self, username):
        user = session.query(User).filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Already Exist')
        
    # Custom validation to check if the provided email already exists       
    def validate_email(self, email):
        user = session.query(User).filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email Address Already Exist')


# Login Form for registered users
class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    
    submit = SubmitField('LOGIN')

# Form for updating user account details
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'svg'])])

    submit = SubmitField('UPDATE')

    # Custom validation to check if the provided username already exists (excluding the current user's username)
    def validate_username(self, username):
        if username.data != current_user.username:
            user = session.query(User).filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username Already Exist')
        
    # Custom validation to check if the provided email already exists (excluding the current user's email)
    def validate_email(self, email):
        if email.data != current_user.email:
            user = session.query(User).filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email Address Already Exist')


# Form for creating a new blog post
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    post_image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png', 'svg'])])
    category = SelectField('Category', coerce=int)

    submit = SubmitField(' CREATE POST')

    # Set category choices dynamically based on available categories in the database
    def set_category_choices(self):
        categories = session.query(Category).all()
        
        self.category.choices = [(category.id, category.category_name) for category in categories]

 # Form for adding comments to blog posts  
class CommentForm(FlaskForm):
    content = TextAreaField('Your Comment', validators=[DataRequired()])
    submit = SubmitField('SUBMIT COMMENT')