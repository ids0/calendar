# pylint: disable=E1101
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskcalendar.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetsPasswordForm
from flaskcalendar.models import User
from flaskcalendar import db, bcrypt
from flaskcalendar.users.utils import save_picture, send_reset_email

usersAPP = Blueprint('users', __name__)


@usersAPP.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)


@usersAPP.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful!', 'danger')
    return render_template('users/login.html', title='Login', form=form)


@usersAPP.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@usersAPP.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    image_file = url_for('static', filename='pics/' + current_user.image_file)
    # Update user
    if form.validate_on_submit():
        # Check if user uploaded a picture
        if form.picture.data:
            # TODO: Delete old picture
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        # Update user info
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        # Fill form with current info
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('users/account.html', title='Account', image_file=image_file, form=form)



@usersAPP.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html', title='Reset Password', form=form)


@usersAPP.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash(f'That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetsPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html', title='Reset Password', form=form)


