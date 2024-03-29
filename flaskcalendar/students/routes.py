# pylint: disable=E1101
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskcalendar import db
from flaskcalendar.models import Student
from flaskcalendar.students.forms import AddStudentForm
from flask_login import login_required, current_user
from flaskcalendar.main.utils import addToHistory
from flaskcalendar.users.utils import isAuthor
studentsAPP = Blueprint('students', __name__)



@studentsAPP.route("/add_student", methods=['GET','POST'])
@login_required
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        author_id = int(current_user.id)
        instance = Student(name=form.name.data, last_name=form.last_name.data, email=form.email.data, phone=form.phone.data, author_id=author_id)
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
        instance = Student.query.filter_by(id=student_id, author_id=current_user.id).first()
        if isAuthor(instance):
            return render_template('students/student.html',title=f'{instance.fullName()} Events',instance=instance)
    return redirect(url_for('students.students'))


@studentsAPP.route("/students")
def students():
    studentsList = []
    if current_user.is_authenticated:
        studentsList = Student.query.filter_by(author_id=current_user.id)
    return render_template('students/students.html', sList = studentsList)


@studentsAPP.route("/edit_student", methods=['GET','POST'])
@login_required
def edit_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        student_id = int(request.form.get("instance_id"))
        instance = Student.query.filter_by(id=student_id, author_id=current_user.id).first()
        if isAuthor(instance):
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
        instance = Student.query.filter_by(id=student_id, author_id=current_user.id).first()
        if isAuthor(instance):
            form.name.data = instance.name
            form.last_name.data = instance.last_name
            form.email.data = instance.email
            form.phone.data = instance.phone
            return render_template('students/edit_student.html', form=form, instance=instance)
    return redirect(url_for('students.students'))


@studentsAPP.route("/students/<int:student_id>/delete", methods=['POST'])
@login_required
def student_delete(student_id):
    instance = Student.query.get_or_404(student_id)
    if isAuthor(instance):
        addToHistory(instance,'delete')
        db.session.delete(instance)
        db.session.commit()
        flash(f"Student has been deleted correctly",'success')
    else:
        flash(f"You're not the author of this Student",'warning')
    return redirect(url_for('students.students'))
