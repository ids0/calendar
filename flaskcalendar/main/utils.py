# pylint: disable=E1101
from flaskcalendar.models import History
from flaskcalendar import db
from datetime import datetime

def addToHistory(instance,action):
    hist = History(time = datetime.utcnow(), entry=(instance), action=action)
    db.session.add(hist)
    db.session.commit()
