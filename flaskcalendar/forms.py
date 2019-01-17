from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskcalendar.models import User, Subjects

from flask import flash

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=10)],render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('User already exists!')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists!')

class LoginForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired(), Length(min=2,max=10)],render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AddProfessorForm(FlaskForm):
    name = StringField('Name', validators=[], render_kw={"placeholder": "Name"})
    last_name = StringField('Last Name', validators=[], render_kw={"placeholder": "Last Name"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    phone = StringField('Phone', validators=[], render_kw={"placeholder": "Phone"})
    submit = SubmitField('Add Professor')

class AddStudentForm(FlaskForm):
    name = StringField('Name', validators=[], render_kw={"placeholder": "Name"})
    last_name = StringField('Last Name', validators=[], render_kw={"placeholder": "Last Name"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    phone = StringField('Phone', validators=[], render_kw={"placeholder": "Phone"})
    submit = SubmitField('Add Student')

class AddSubjectForm(FlaskForm):
    subject= StringField('Subject', validators=[], render_kw={"placeholder": "Subject"})
    submit = SubmitField('Add Subject')

    def validate_subject(self,subject):
        subject = Subjects.query.filter_by(subject=subject.data).first()
        if subject:
            #FIXME: wtf was this
            flash(f'forms.py don\'t like thi!', 'danger')
            raise ValidationError('Subject already exists!')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=10)],render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    picture = FileField('Update Profile Pic', validators=[FileAllowed(['jpg','png'])], render_kw={"placeholder": "Update Profile Picture"})
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('User already exists!')
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists!')

