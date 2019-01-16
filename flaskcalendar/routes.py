from flask import render_template, url_for, flash, redirect, request
from flaskcalendar import app, db, bcrypt
from flaskcalendar.forms import RegistrationForm, LoginForm, AddProfessorForm, AddStudentForm, AddSubjectForm, UpdateAccountForm
from flaskcalendar.models import User,Professor,Student,Subjects,ProfessorSubjects,Task, History
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
posts = []
from functools import wraps


def addHistory(instance):
    hist = History(time = datetime.utcnow(), entry=(instance), action="add")
    db.session.add(hist)
    db.session.commit()



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts = posts)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register',form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful!', 'danger')
    return render_template('login.html', title='Login',form=form)

@app.route("/history", methods=['GET','POST'])
@login_required
def history():
    events = History.query.order_by("id desc")
    return render_template('history.html', events = events)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    image_file = url_for('static', filename='pics/' + current_user.image_file)
    # Update user
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated','success')
        # POST/ GET REDIRECT  redirect not update
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/add", methods=['GET','POST'])
@login_required
def add():
    return render_template('add.html', title='Add')


@app.route("/add_professors", methods=['GET','POST'])
def add_professors():
    form = AddProfessorForm()
    sList = Subjects.query.filter_by()
    if form.validate_on_submit():
        instance = Professor(name=form.name.data,last_name = form.last_name.data, email=form.email.data, phone=form.phone.data)
        db.session.add(instance)
        # TODO: Maybe only add to history after confirmation
        addHistory(instance)
        db.session.commit()

        # Link professor to subjects if any selected
        if request.form.get("Subject"):
            for subject_id in request.form.getlist("Subject"):
                subject_id = int(subject_id)
                db.session.add(ProfessorSubjects(professor_id=instance.id,subject_id=subject_id))
                db.session.commit()

        flash(f'{instance.name} {instance.last_name} added as a {instance.__class__.__name__}!', 'success')
        return redirect(url_for('add'))
    return render_template('add_professors.html',form=form,subjectsList = sList)

@app.route("/add_students", methods=['GET','POST'])
def add_students():
    form = AddStudentForm()
    if form.validate_on_submit():
        instance = Student(name=form.name.data,last_name = form.last_name.data, email=form.email.data, phone=form.phone.data)
        db.session.add(instance)
        addHistory(instance)    # If added after session.commit() something fail
        db.session.commit()

        flash(f'{instance.name} {instance.last_name} added as a {instance.__class__.__name__}!', 'success')
        return redirect(url_for('add'))
    return render_template('add_students.html',form=form)

@app.route("/add_subjects", methods=['GET','POST'])
def add_subjects():
    form = AddSubjectForm()
    if form.validate_on_submit():
        instance = Subjects(subject=form.subject.data)
        addHistory(instance)
        db.session.add(instance)
        db.session.commit()
        flash(f'{form.subject.data} added!', 'success')
        return redirect(url_for('add'))
    return render_template('add_subjects.html',form=form)

@app.route("/link", methods=['GET','POST'])
def link():
    professorsList = Professor.query
    subjectsList = Subjects.query
    if request.form.getlist("Subject") and request.form.get("Professor"):
        for subject_id in request.form.getlist("Subject"):
            subject_id = int(subject_id)
            professor_id = int(request.form.get("Professor"))
            # Check if realationship doen's exist already
            if ProfessorSubjects.query.filter_by(professor_id=professor_id,subject_id=subject_id).first():
                flash(f'{professorsList.filter_by(id=professor_id).first().name} {professorsList.filter_by(id=professor_id).first().name_last} not linked to {subjectsList.filter_by(id=subject_id).first().subject}!', 'danger')
            else:
                instance = ProfessorSubjects(professor_id=professor_id,subject_id=subject_id)
                db.session.add(instance)
                db.session.commit()
                flash(f'{professorsList.filter_by(id=professor_id).first().name} {professorsList.filter_by(id=professor_id).first().last_name}linked to {subjectsList.filter_by(id=subject_id).first().subject}!', 'success')

    return render_template('link.html', professorsList=professorsList, subjectsList=subjectsList)

@app.route("/edit", methods=['GET','POST'])
def edit():
    professorsList = Professor.query
    subjectsList = Subjects.query
    studentsList = Student.query

    if request.args.get('Professor'):
        return redirect(url_for('edit_professor', Professor=request.args.get('Professor')))
    elif request.args.get('Subject'):
        return redirect(url_for('edit_subject', Subject=request.args.get('Subject')))
    elif request.args.get('Student'):
        return redirect(url_for('edit_Student', Subject=request.args.get('Studen')))

    return render_template('edit.html', professorsList=professorsList, subjectsList=subjectsList, studentsList=studentsList)

@app.route("/edit_professor", methods=['GET','POST'])
def edit_professor():
    form = AddProfessorForm()
    print("Yeeeey~~~~~")
    print(request.referrer)

    if form.validate_on_submit():
        professor_id = int(request.form.get("instance_id"))
        instance = Professor.query.filter_by(id=professor_id).first()
        instance.name = form.name.data
        instance.last_name  = form.last_name.data
        instance.email  = form.email.data
        instance.phone = form.phone.data
        db.session.commit()
        flash(f"{instance.name} {instance.last_name}' account has been updated",'success')
        # POST/ GET redirect better to use redirect instead update
        # TODO: Redirect to previous page

        return redirect(url_for('edit'))
    elif request.method == 'GET' and request.args.get('Professor'):
        professor_id = int(request.args.get('Professor'))
        instance = Professor.query.filter_by(id=professor_id).first()
        form.name.data = instance.name
        form.last_name.data = instance.last_name
        form.email.data = instance.email
        form.phone.data = instance.phone
        return render_template('edit_professor.html', form=form, instance=instance)
    elif request.args.to_dict() == {}:
        # TODO: List of professors
        professorsList = Professor.query
        return render_template('edit_professor.html', pList = professorsList)
    else:
        flash(f"Something went wrong",'danger')


    return redirect(url_for('edit'))
