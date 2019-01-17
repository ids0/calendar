from datetime import datetime
from flaskcalendar import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.Integer)
    # TODO: Relationship to get professor.task or something
    # subjects_id = db.Column(db.Integer, db.ForeignKey('subjects.id'),nullable=True)

    def __repr__(self):
        return f"Professor('{self.name}' '{self.last_name}')"

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    # subjects_id = db.Column(db.Integer, db.ForeignKey('subjects.id'),nullable=True)

    def __repr__(self):
        return f"Student('{self.name}', '{self.last_name}')"

class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    # professors = db.relationship('Prof', backref='professors', lazy=True)

    def __repr__(self):
        return f"Subjects('{self.id}', '{self.subject}')"

class ProfessorSubjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, nullable=False)
    subject_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Post('{self.professor_id}', '{self.subject_id}')"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    subject_id = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # TODO: Relationship to get task.proffesor or something
    # subjects_id = db.Column(db.Integer, db.ForeignKey('subjects.id'),nullable=True)

    def __repr__(self):
        return f"Post('{self.professor_id}', '{self.student_id}', '{self.subject_id}')"

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.PickleType, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    action = db.Column(db.String(15), nullable=False,  default='change')

    def __repr__(self):
        return f"History('{self.id}', '{self.entry}','{self.time}')"
