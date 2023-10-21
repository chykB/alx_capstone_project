from flask import Flask
import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from sqlalchemy.exc import IntegrityError
from connection import session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required




app = Flask(__name__)
app.config['SECRET_KEY'] = '875ef99af5d26318088c80ac0d09bc28'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def user_loader(user_id):
    from models import User
    return session.query(User).get(int(user_id))






@app.route('/')
def index():
    from models import Post
    posts = session.query(Post).all()
    return render_template('index.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    from forms import RegistrationForm
    from models import User
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        session.add(user)
        session.commit()
        flash('Account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('login'))
    flash('Password does not match', 'error')
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    from forms import LoginForm
    from models import User
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Login Unsuccessful. Please check email and password', 'error')
    return render_template('login.html', title='Login', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    from forms import UpdateAccountForm
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        session.commit()
        flash('Your Account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)



def save_post_image(form_post_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_post_image.filename)
    post_image = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', post_image)
    form_post_image.save(picture_path)
    return post_image



@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    from forms import PostForm
    from models import Post, Category
    form = PostForm()

    # form.set_category_choices()
    image_file = None

    if form.validate_on_submit(): 
        if form.post_image.data:
            image_file = save_post_image(form.post_image.data)
        
        category = session.query(Category).get(form.category.data)
        post = Post(
            title=form.title.data, 
            content=form.content.data, 
            description=form.description.data, 
            post_image_file=image_file, 
            category=category, 
            author=current_user
            )

        
        try:
            session.add(post)
            session.commit()
            flash('Your post has been created', 'success')
            return redirect(url_for('index'))
        
        except IntegrityError as e:
            session.rollback()
            flash('description exceed maximum character', 'error')

    post_photo = image_file if image_file is not None else url_for('static', 
                                                                        filename='images/default_post_image.jpg',)
       
    return render_template('create_post.html', form=form, post_photo=post_photo, legend='New POST')



@app.route('/post/<int:post_id>')
def post(post_id):
    from models import Post
    post = session.query(Post).get(post_id)

    if post is None:
        return render_template('404.html'), 404

    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    from models import Post
    from forms import PostForm
    post = session.query(Post).get(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.description = form.description.data
        session.commit()
        flash('Your post has been update', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.description.data = post.description



    return render_template('update_post.html', form=form,  legend='Update Post')






if __name__== '__main__':
    app.run(debug=True)