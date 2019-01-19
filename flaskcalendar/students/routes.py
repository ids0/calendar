# pylint: disable=E1101
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskcalendar import db
from flaskcalendar.models import Student
from flaskcalendar.students.forms import AddStudentForm
from flask_login import login_required
from flaskcalendar.main.utils import addToHistory

studentsAPP = Blueprint('students', __name__)



@studentsAPP.route("/add_student", methods=['GET','POST'])
@login_required
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        instance = Student(name=form.name.data, last_name=form.last_name.data, email=form.email.data, phone=form.phone.data)
        db.session.add(instance)
        addToHistory(instance,'add')
        db.session.commit()
        flash(f'{instance.name} {instance.last_name} added as a {instance.__class__.__name__}!', 'success')
        return redirect(url_for('students.students'))
    return render_template('students/add_student.html',form=form)

@studentsAPP.route("/student")
def student():
    if request.method == 'GET' and request.args.get('id'):
        student_id = int(request.args.get('id'))
        instance = Student.query.filter_by(id=student_id).first()
        return render_template('students/student.html',title=f'{instance.fullName()} Events',instance=instance)
    return redirect(url_for('students.students'))

@studentsAPP.route("/students")
def students():
    studentsList = Student.query
    return render_template('students/students.html', sList = studentsList)


@studentsAPP.route("/edit_student", methods=['GET','POST'])
@login_required
def edit_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        student_id = int(request.form.get("instance_id"))
        instance = Student.query.filter_by(id=student_id).first()
        instance.name = form.name.data
        instance.last_name  = form.last_name.data
        instance.email  = form.email.data
        instance.phone = form.phone.data
        addToHistory(instance,'edit')
        db.session.commit()
        flash(f"{instance.fullName()} account has been updated",'success')
        return redirect(url_for('students.students'))
    elif request.method == 'GET' and request.args.get('Student'):
        student_id = int(request.args.get('Student'))
        instance = Student.query.filter_by(id=student_id).first()
        form.name.data = instance.name
        form.last_name.data = instance.last_name
        form.email.data = instance.email
        form.phone.data = instance.phone
        return render_template('students/edit_student.html', form=form, instance=instance)
    return redirect(url_for('students.students'))
