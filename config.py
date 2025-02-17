import keys
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = keys.APP_SECRET_KEY
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)