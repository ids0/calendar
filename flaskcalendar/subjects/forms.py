from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from flask import flash
from flaskcalendar.models import Subject
from flask_login import current_user


class AddSubjectForm(FlaskForm):
    subject= StringField('Subject', validators=[DataRequired()], render_kw={"placeholder": "Subject"})
    submit = SubmitField('Add Subject')

    def validate_subject(self,subject):
        subject = Subject.query.filter_by(subject=subject.data).first()
        if subject and subject.author_id == current_user.id:
            raise ValidationError('Subject already exists!')
