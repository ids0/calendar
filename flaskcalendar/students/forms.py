from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email



class AddStudentForm(FlaskForm):
    name = StringField('Name', validators=[], render_kw={"placeholder": "Name"})
    last_name = StringField('Last Name', validators=[], render_kw={"placeholder": "Last Name"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    phone = StringField('Phone', validators=[], render_kw={"placeholder": "Phone"})
    submit = SubmitField('Add Student')
