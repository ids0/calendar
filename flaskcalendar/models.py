# TODO: Search page events / pages
# TODO: Create events only with professor's subjects
# TODO: Link with students / professors for alerts
# TODO: Cleanup HTML
# TODO: Subtemplates
# TODO: README.md


# pylint: disable=E1101
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskcalendar import db, login_manager
from flask import current_app
from flask_login import UserMixin, current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    events = db.relationship('Event', backref='author', lazy=True, cascade="all, delete-orphan")
    professors = db.relationship('Professor', backref='author', lazy=True, cascade="all, delete-orphan")
    students = db.relationship('Student', backref='author', lazy=True, cascade="all, delete-orphan")
    subjects = db.relationship('Subject', backref='author', lazy=True, cascade="all, delete-orphan")
    history = db.relationship('History', backref='author', lazy=True, cascade="all, delete-orphan")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.Integer)
    events = db.relationship('Event', backref='professor', lazy=True, cascade="all, delete-orphan")
    subjects = db.relationship('ProfessorSubjects', backref='professor', lazy=True, cascade="all, delete-orphan")
    author_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Professor('{self.name}' '{self.last_name}')"

    def fullName(self):
        return f"{self.name} {self.last_name}"


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    events = db.relationship('Event', backref='student', lazy=True, cascade="all, delete-orphan")
    author_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Student('{self.name}', '{self.last_name}')"

    def fullName(self):
        return f"{self.name} {self.last_name}"


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    events = db.relationship('Event', backref='subject', lazy=True, cascade="all, delete-orphan")
    professors = db.relationship('ProfessorSubjects', backref='subject', lazy=True, cascade="all, delete-orphan")
    author_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def fullName(self):
        return f"{self.subject}"

    def __repr__(self):
        return f"Subjects('{self.id}', '{self.subject}')"


class ProfessorSubjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    # author_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Maybe not necessary

    def __repr__(self):
        return f"ProfessorSubjects('{self.professor_id}', '{self.subject_id}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    author_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Boolean, nullable=False,  default=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # TODO: boolean field if didn't notify yet, default true

    def __repr__(self):
        return f"Event('{self.professor_id}' '{self.student_id}', '{self.subject_id}', {self.time}')"

    def __srt__(self):
        return f"Event('{self.professor.name}' '{self.student.name}', '{self.subject.subject}, {self.time}')"


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.PickleType, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    action = db.Column(db.String(15), nullable=False,  default='change')
    author_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"History('{self.id}', '{self.entry}','{self.time}')"
