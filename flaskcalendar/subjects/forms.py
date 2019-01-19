from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from flask import flash
from flaskcalendar.models import Subject


class AddSubjectForm(FlaskForm):
    subject= StringField('Subject', validators=[DataRequired()], render_kw={"placeholder": "Subject"})
    submit = SubmitField('Add Subject')

    def validate_subject(self,subject):
        subject = Subject.query.filter_by(subject=subject.data).first()
        if subject:
            #FIXME: wtf was this
            flash(f'forms.py don\'t like thi!', 'danger')
            raise ValidationError('Subject already exists!')
