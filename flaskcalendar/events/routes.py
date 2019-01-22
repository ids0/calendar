# pylint: disable=E1101
from flask import Blueprint
from datetime import datetime, timedelta
from flask import render_template, url_for, flash, redirect, request, abort
from flaskcalendar.models import Professor, Student, Subject, Event
from flask_login import current_user, login_required
from flaskcalendar.main.utils import addToHistory
from flaskcalendar import db
from flaskcalendar.users.utils import isAuthor
eventsAPP = Blueprint('events', __name__)

# Time delta to modify server time
SERVER_TIME_CORRECTION = timedelta(hours=3)

@eventsAPP.route("/events/create", methods=['GET','POST'])
@login_required
def create_event():
    professorsList, subjectsList, studentsList = Professor.query.filter_by(author_id=current_user.id), Subject.query.filter_by(author_id=current_user.id), Student.query.filter_by(author_id=current_user.id)
    time = datetime.now()-SERVER_TIME_CORRECTION
    time = time.strftime("%Y-%m-%dT%H:%M")
    # ProfessorSubjectsList = ProfessorSubjects.query # TODO: What to do with this, maybe add ajax
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
    return render_template('events/create_event.html',time=time, title='Create Event',professorsList=professorsList, subjectsList=subjectsList, studentsList=studentsList)


@eventsAPP.route("/events")
def events():
    eventsList =[]
    if current_user.is_authenticated:
        eventsList = Event.query.filter_by(author_id=current_user.id).order_by("id desc")
    return render_template('events/events.html', title='Events', eList=eventsList)


@eventsAPP.route("/event")
def event():
    return redirect(url_for("events"))


@eventsAPP.route("/event/<int:event_id>")
@login_required
def event_id(event_id):
    instance = Event.query.get_or_404(event_id)
    print(current_user.id)
    print(instance.author_id)
    if isAuthor(instance):
        print('yey')
        return render_template('events/event.html', event=instance)
    abort(403)


@eventsAPP.route("/event/<int:event_id>/edit", methods=['GET','POST'])
@login_required
def event_update(event_id):
    instance = Event.query.get_or_404(event_id)
    if not isAuthor(instance):
        abort(403)
    professorsList, subjectsList, studentsList = Professor.query.filter_by(author_id=current_user.id), Subject.query.filter_by(author_id=current_user.id), Student.query.filter_by(author_id=current_user.id)
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
    return render_template('events/edit_event.html', title='Edit Event', professorsList=professorsList, subjectsList=subjectsList, studentsList=studentsList, event=instance)


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
