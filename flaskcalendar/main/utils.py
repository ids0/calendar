# pylint: disable=E1101
from flaskcalendar.models import History
from flaskcalendar import db
from datetime import datetime
from flask_login import current_user

def addToHistory(instance,action):
    hist = History(time = datetime.utcnow(), entry=(instance), author_id=current_user.id, action=action)
    db.session.add(hist)
    db.session.commit()
