import secrets
import os
from PIL import Image
from flask_login import current_user
from flaskcalendar import mail
from flask_mail import Message
from flask import url_for, current_app

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(current_user.id) + '_' + random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static\pics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@test-calendar.com', recipients=[user.email])
    msg.body = f'''To reset your password
{url_for('users.reset_token', token=token, _external=True)}
'''
    mail.send(msg)

def isAuthor(instance,current_user=current_user):
    if instance and instance.author_id == current_user.id:
        return True
    else:
        return False