# pylint: disable=E1101
from flaskcalendar.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()


def create_app(config_class=Config):
    application = app = Flask(__name__)
    app.config.from_object(Config)

    from flaskcalendar.users.routes import usersAPP
    from flaskcalendar.main.routes import mainAPP
    from flaskcalendar.events.routes import eventsAPP
    from flaskcalendar.professors.routes import professorsAPP
    from flaskcalendar.students.routes import studentsAPP
    from flaskcalendar.subjects.routes import subjectsAPP
    from flaskcalendar.errors.handlers import errorsAPP
    app.register_blueprint(usersAPP)
    app.register_blueprint(mainAPP)
    app.register_blueprint(eventsAPP)
    app.register_blueprint(professorsAPP)
    app.register_blueprint(studentsAPP)
    app.register_blueprint(subjectsAPP)
    app.register_blueprint(errorsAPP)
    db.init_app(application)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    return app