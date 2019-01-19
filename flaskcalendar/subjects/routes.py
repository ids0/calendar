# pylint: disable=E1101
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskcalendar import db
from flaskcalendar.models import Subject
from flaskcalendar.subjects.forms import AddSubjectForm
from flask_login import login_required
from flaskcalendar.main.utils import addToHistory

subjectsAPP = Blueprint('subjects', __name__)

@subjectsAPP.route("/subjects")
def subjects():
    subjectsList = Subject.query
    return render_template('subjects/subjects.html', sjList = subjectsList)


@subjectsAPP.route("/add_subject", methods=['GET','POST'])
@login_required
def add_subject():
    form = AddSubjectForm()
    if form.validate_on_submit():
        instance = Subject(subject=form.subject.data)
        db.session.add(instance)
        addToHistory(instance,'add')
        db.session.commit()
        flash(f'{form.subject.data} added!', 'success')
        return redirect(url_for('subjects.subjects'))
    return render_template('subjects/add_subject.html', form=form)


@subjectsAPP.route("/edit_subject", methods=['GET','POST'])
@login_required
def edit_subject():
    form = AddSubjectForm()
    if form.validate_on_submit():
        subject_id = int(request.form.get("instance_id"))
        instance = Subject.query.filter_by(id=subject_id).first()
        instance.subject = form.subject.data
        addToHistory(instance,'edit')
        db.session.commit()
        flash(f"{instance.subject}' has been updated",'success')
        return redirect(url_for('subjects.subjects'))
    elif request.method == 'GET' and request.args.get('Subject'):
        subject_id = int(request.args.get('Subject'))
        instance = Subject.query.filter_by(id=subject_id).first()
        form.subject.data = instance.subject
        return render_template('edit_subject.html', form=form, instance=instance)
    return redirect(url_for('subjects/subjects.subjects'))


@subjectsAPP.route("/subject")
def subject():
    if request.method == 'GET' and request.args.get('id'):
        subject_id = int(request.args.get('id'))
        instance = Subject.query.filter_by(id=subject_id).first()
        return render_template('subject.html',title=f'{instance.subject} Events',instance=instance)
    return redirect(url_for('subjects/subjects.subjects'))


