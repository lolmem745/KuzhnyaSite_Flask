from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

# Association table for many-to-many relationship between users and games
user_games = db.Table('user_games',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True)
)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    riot_user = db.relationship("RiotAccountInfoUser", backref="user", uselist=False, cascade="all, delete-orphan")
    games = db.relationship('Games', secondary=user_games, backref=db.backref('participants', lazy='dynamic'))

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
    id = db.Column(db.Integer, primary_key=True)
    tournament_name = db.Column(db.String(30), nullable=False)
    games = db.relationship('Games', backref='tournament', lazy=True, cascade="all, delete-orphan")

    def __init__(self, tournament_name: str):
        self.tournament_name = tournament_name

    def get_closest_game(self):
        now = datetime.now()
        closest_game = min(self.games, key=lambda game: abs(game.game_time - now))
        return closest_game


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(30), nullable=False)
    game_time = db.Column(db.DateTime, nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)

    def __init__(self, game_name: str, game_time: datetime, tournament_id: int):
        self.game_name = game_name
        self.game_time = game_time
        self.tournament_id = tournament_id

    def formatted_game_time(self):
        return self.game_time.strftime('%H:%M %d-%m-%Y')