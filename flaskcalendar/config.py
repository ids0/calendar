import json
from sys import platform

if platform == "linux" or platform == "linux2":
    with open("/etc/config.json") as config_file:
        config = json.load(config_file)
elif platform == "win32":
    import os
    path = os.path.join(os.pardir,'config.json')
    with open(path) as config_file:
        config = json.load(config_file)

class Config():
    SECRET_KEY = config.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get('EMAIL_USER')
    MAIL_PASSWORD = config.get('EMAIL_PASS')
