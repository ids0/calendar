# pylint: disable=E1101
from flaskcalendar.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

application = app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail(app)




from flaskcalendar.users.routes import usersAPP
from flaskcalendar.main.routes import mainAPP
from flaskcalendar.events.routes import eventsAPP
from flaskcalendar.professors.routes import professorsAPP
from flaskcalendar.students.routes import studentsAPP
from flaskcalendar.subjects.routes import subjectsAPP

app.register_blueprint(usersAPP)
app.register_blueprint(mainAPP)
app.register_blueprint(eventsAPP)
app.register_blueprint(professorsAPP)
app.register_blueprint(studentsAPP)
app.register_blueprint(subjectsAPP)
