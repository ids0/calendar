# pylint: disable=E1101
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskcalendar import db
from flaskcalendar.models import Professor, Student, Subject, ProfessorSubjects, Event, History
from flask_login import login_required
from datetime import timedelta
import itertools

mainAPP = Blueprint('main', __name__)


@mainAPP.route("/")
@mainAPP.route("/home")
def home():
    # Query dates already in order
    events = Event.query.order_by("time")
    dates = []
    time_delta = timedelta(hours=3)
    for a, b in itertools.combinations(events, 2):
        if -time_delta < a.time - b.time  < time_delta:
            if a.student == b.student:
                flash(f"Student: {a.student.fullName()} has 2 events close to each other, event {a.id} and {b.id} ",'danger')
            elif a.professor == b.professor:
                flash(f"Professor: {a.professor.fullName()} has 2 events close to each other, event {a.id} and {b.id} ",'danger')
        if a.time.date() not in dates:
            dates.append(a.time.date())
        if b.time.date() not in dates:
            dates.append(b.time.date())
    return render_template('home.html', events= events, dates=dates)

@mainAPP.route("/about")
def about():
    return render_template('about.html')


@mainAPP.route("/history", methods=['GET','POST'])
def history():
    # Get events in desc order, first most recent
    events = History.query.order_by("id desc")
    return render_template('history.html', events=events)


@mainAPP.route("/add", methods=['GET','POST'])
@login_required
def add():
    return render_template('add.html', title='Add')

@mainAPP.route("/link", methods=['GET','POST'])
def link():
    professorsList = Professor.query
    subjectsList = Subject.query
    if request.form.getlist("Subject") and request.form.get("Professor"):
        # If multiple subjects selected
        for subject_id in request.form.getlist("Subject"):
            subject_id = int(subject_id)
            professor_id = int(request.form.get("Professor"))
            # Check if realationship doen's exist already
            if ProfessorSubjects.query.filter_by(professor_id=professor_id, subject_id=subject_id).first():
                flash(f'{professorsList.filter_by(id=professor_id).first().fullName()} already linked to {subjectsList.filter_by(id=subject_id).first().subject}!', 'danger')
            else:
                instance = ProfessorSubjects(professor_id=professor_id, subject_id=subject_id)
                db.session.add(instance)
                db.session.commit()
                flash(f'{professorsList.filter_by(id=professor_id).first().fullName()} linked to {subjectsList.filter_by(id=subject_id).first().subject}!', 'success')
    return render_template('link.html', professorsList=professorsList, subjectsList=subjectsList)

@mainAPP.route("/edit", methods=['GET','POST'])
def edit():
    professorsList, subjectsList, studentsList = Professor.query, Subject.query, Student.query
    if request.args.get('Professor'):
        return redirect(url_for('professors.edit_professor', Professor=request.args.get('Professor')))
    elif request.args.get('Subject'):
        return redirect(url_for('subjects.edit_subject', Subject=request.args.get('Subject')))
    elif request.args.get('Student'):
        return redirect(url_for('students.edit_student', Student=request.args.get('Student')))
    return render_template('edit.html', professorsList=professorsList, subjectsList=subjectsList, studentsList=studentsList)

