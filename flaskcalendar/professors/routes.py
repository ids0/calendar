# pylint: disable=E1101
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskcalendar import db
from flaskcalendar.models import Professor, Subject, ProfessorSubjects
from flask_login import login_required, current_user
from flaskcalendar.professors.forms import AddProfessorForm
from flaskcalendar.main.utils import addToHistory
from flaskcalendar.users.utils import isAuthor
professorsAPP = Blueprint('professors', __name__)



@professorsAPP.route("/add_professor", methods=['GET','POST'])
@login_required
def add_professor():
    form = AddProfessorForm()
    sList = Subject.query.filter_by(author_id=current_user.id)
    if form.validate_on_submit():
        author_id = int(current_user.id)
        instance = Professor(name=form.name.data, last_name=form.last_name.data, email=form.email.data, phone=form.phone.data, author_id=author_id)
        db.session.add(instance)
        # Have to add before commit, otherwise db get corrupted
        addToHistory(instance,'add')
        db.session.commit()
        # Link professor to Subject if any selected
        if request.form.get("Subject"):
            for subject_id in request.form.getlist("Subject"):
                subject_id = int(subject_id)
                db.session.add(ProfessorSubjects(professor_id=instance.id,subject_id=subject_id))
                db.session.commit()
        flash(f'{instance.name} {instance.last_name} added as a {instance.__class__.__name__}!', 'success')
        return redirect(url_for('professors.professors'))
    return render_template('professors/add_professor.html',form=form, subjectsList=sList)


@professorsAPP.route("/professor")
def professor():
    if request.method == 'GET' and request.args.get('id'):
        professor_id = int(request.args.get('id'))
        instance = Professor.query.filter_by(id=professor_id).first()
        if isAuthor(instance):
            return render_template('professors/professor.html',title=f'{instance.fullName()} Events', instance=instance)
    return redirect(url_for('professors.professors'))


@professorsAPP.route("/professors")
def professors():
    professorsList = []
    if current_user.is_authenticated:
        professorsList = Professor.query.filter_by(author_id=current_user.id)
    return render_template('professors/professors.html', pList = professorsList)


@professorsAPP.route("/edit_professor", methods=['GET','POST'])
@login_required
def edit_professor():
    form = AddProfessorForm()
    if form.validate_on_submit():
        professor_id = int(request.form.get("instance_id"))
        instance = Professor.query.filter_by(id=professor_id).first()
        if isAuthor(instance):
            instance.name = form.name.data
            instance.last_name  = form.last_name.data
            instance.email  = form.email.data
            instance.phone = form.phone.data
            addToHistory(instance,'edit')
            db.session.commit()
            flash(f"{instance.fullName()} account has been updated",'success')
            return redirect(url_for('professors.professors'))
    elif request.method == 'GET' and request.args.get('Professor'):
        professor_id = int(request.args.get('Professor'))
        instance = Professor.query.filter_by(id=professor_id).first()
        if isAuthor(instance):
            form.name.data = instance.name
            form.last_name.data = instance.last_name
            form.email.data = instance.email
            form.phone.data = instance.phone
            return render_template('professors/edit_professor.html', form=form, instance=instance)
    return redirect(url_for('professors.professors'))


@professorsAPP.route("/professors/<int:professor_id>/delete", methods=['POST'])
@login_required
def professor_delete(professor_id):
    instance = Professor.query.get_or_404(professor_id)
    if isAuthor(instance):
        addToHistory(instance,'delete')
        db.session.delete(instance)
        db.session.commit()
        flash(f"Professor has been deleted correctly",'success')
    else:
        flash(f"You're not the author of this Professor",'warning')
    return redirect(url_for('professors.professors'))