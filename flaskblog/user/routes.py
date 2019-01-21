from flask import render_template, request, Blueprint, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.user.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog import db, bcrypt
from flaskblog.models.user import User
from flaskblog.models.post import Post
from flaskblog.user.utils import save_picture

user: Blueprint = Blueprint('user', __name__)


@user.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    registration_from = RegistrationForm()
    if registration_from.validate_on_submit():
        encrypted_pass = bcrypt.generate_password_hash(registration_from.password.data).decode('utf-8')
        user_data = User(username=registration_from.username.data, email=registration_from.email.data,
                         password=encrypted_pass)
        db.session.add(user_data)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('user.login'))
    return render_template('register.html', form=registration_from)


@user.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_exist = User.query.filter_by(email=login_form.email.data).first()
        if user_exist and bcrypt.check_password_hash(user_exist.password, login_form.password.data):
            login_user(user_exist, remember=login_form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful, Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=login_form)


@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@user.route("/account", methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
