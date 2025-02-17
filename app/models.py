from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    riot_user = db.relationship("RiotAccountInfoUser", backref="user", uselist=False, cascade="all, delete-orphan")

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class RiotAccountInfoUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    riot_id = db.Column(db.String(50), unique=True, nullable=False)
    role_1 = db.Column(db.String(3))
    role_2 = db.Column(db.String(3))
    region = db.Column(db.String(4))
    icon_id = db.Column(db.Integer)


class Tournaments(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    tournament_name = db.Column(db.String(30))
    game_name = db.Column(db.String(30))
    game_time = db.Column(db.String(5))

    def __init__(self, tournament_name: str, game_name: str, game_time: str):
        self.tournament_name = tournament_name
        self.game_name = game_name
        self.game_time = game_time