# pylint: disable=E1101
from flask import Blueprint
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, abort
from flaskcalendar.models import Professor, Student, Subject, Event
from flask_login import current_user, login_required
from flaskcalendar.main.utils import addToHistory
from flaskcalendar import db

eventsAPP = Blueprint('events', __name__)


@eventsAPP.route("/events/create", methods=['GET','POST'])
@login_required
def create_event():
    professorsList, subjectsList, studentsList = Professor.query, Subject.query, Student.query
    time = datetime.now().strftime("%Y-%m-%dT%H:%M")
    # TODO: What to do with this, maybe add ajax
    # ProfessorSubjectsList = ProfessorSubjects.query
    if request.method == 'POST':
        professor_id, student_id, subject_id = request.form.get('Professor'), request.form.get('Student'), request.form.get('Subject')
        time = request.form.get('Time')
        author_id = int(current_user.id)
        # TODO: Daytime saving ???
        time_dt = datetime.strptime(time,"%Y-%m-%dT%H:%M")
        instance = Event(professor_id=professor_id, student_id=student_id, subject_id=subject_id, author_id=author_id, time=time_dt)
        db.session.add(instance)
        addToHistory(instance,'add')
        db.session.commit()
        professor_obj, student_obj, subject_obj  = professorsList.filter_by(id=professor_id).first(), studentsList.filter_by(id=student_id).first(), subjectsList.filter_by(id=subject_id).first()
        flash(f"Event created for {professor_obj.fullName()} with {student_obj.fullName()} of {subject_obj.subject} at {instance.time}",'success')
        return redirect(url_for('events.create_event'))
    return render_template('create_event.html',time=time, title='Create Event',professorsList=professorsList, subjectsList=subjectsList, studentsList=studentsList)


@eventsAPP.route("/events")
def events():
    eventsList = Event.query.order_by("id desc")
    return render_template('events.html', title='Events', eList = eventsList)


@eventsAPP.route("/event")
def event():
    return redirect(url_for("events"))

@eventsAPP.route("/event/<int:event_id>")
def event_id(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event.html', event = event)

@eventsAPP.route("/event/<int:event_id>/edit", methods=['GET','POST'])
@login_required
def event_update(event_id):
    instance = Event.query.get_or_404(event_id)
    if instance.author != current_user:
        abort(403)
    professorsList, subjectsList, studentsList = Professor.query, Subject.query, Student.query
    if request.method == 'POST' and request.values:
        # Can make this part shorter but less clear
        instance.professor_id = int(request.form.get('Professor'))
        instance.student_id = int(request.form.get('Student'))
        instance.subject_id = int(request.form.get('Subject'))
        time = request.form.get('Time')
        time_dt = datetime.strptime(time,"%Y-%m-%dT%H:%M")
        instance.time = time_dt
        addToHistory(instance,'edit')
        db.session.commit()
        flash(f"Event {instance.id} has been updated correctly",'success')
        return redirect(url_for('events.event_id', event_id=instance.id))
    # TODO: Delete button in edit page
    return render_template('edit_event.html', title='Edit Event',professorsList=professorsList, subjectsList=subjectsList, studentsList=studentsList, event=instance)

@eventsAPP.route("/event/<int:event_id>/delete", methods=['POST'])
@login_required
def event_delete(event_id):
    instance = Event.query.get_or_404(event_id)
    if instance.author != current_user:
        abort(403)
    addToHistory(instance,'delete')
    db.session.delete(instance)
    db.session.commit()
    flash(f"Event has been deleted correctly",'success')
    return redirect(url_for('events.events'))
