import random
import re
from datetime import timedelta
from typing import List

from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import keys
import riot_funcs

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = keys.APP_SECRET_KEY
app.permanent_session_lifetime = timedelta(days=1)
app.app_context().push()
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username / Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
    ])
    password_repeat = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


def clean_input(input_string: str) -> str:
    # Удаляем невидимые символы Unicode, такие как ZERO WIDTH SPACE
    cleaned = re.sub(r'[\u200b\u200c\u200d\u2060\u2061]', '', input_string)
    # Убираем любые другие неотображаемые символы
    cleaned = ''.join(c for c in cleaned if c.isprintable())
    return cleaned.strip()


def get_user_by_email_or_username(identifier: str):
    return users.query.filter((users.email == identifier) | (users.username == identifier)).first()


class users(UserMixin, db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    riot_user = db.relationship("riot_account_info_user", backref=backref("users", uselist=False))

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class riot_account_info_user(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(users.id))

    riot_id = db.Column(db.String(50))
    role_1 = db.Column(db.String(3))
    role_2 = db.Column(db.String(3))
    region = db.Column(db.String(4))
    icon_id = db.Column(db.Integer)


class tournaments(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    tournament_name = db.Column(db.String(30))
    game_name = db.Column(db.String(30))
    game_time = db.Column(db.String(5))

    def __init__(self, tournament_name: str, game_name: str, game_time: str):
        self.tournament_name = tournament_name
        self.game_name = game_name
        self.game_time = game_time


def get_user_tournaments(user_id: int) -> List[tournaments]:
    return tournaments.query.all()


@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_email_or_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            session["username"] = user.username 
            return redirect(url_for("home"))
        else:
            flash("Неверный логин или пароль")
            return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        found_user = get_user_by_email_or_username(email) or get_user_by_email_or_username(username)
        if found_user:
            flash("Пользователь с таким ником/почтой уже зарегестрирован")
            return redirect(url_for("register"))
        else:
            user = users(username, email, password)
            db.session.add(user)
            db.session.commit()
            flash("Успешная регистрация")
            return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/profile")
@login_required
def profile():
    tournament_list = get_user_tournaments(current_user.id)
    return render_template("profile.html", tournament_list=tournament_list, user=current_user)


@app.route("/connect", methods=["GET", "POST"])
@login_required
def connect():
    if request.method == "POST":
        riotid = clean_input(request.form["riotid"])
        role_1 = request.form["select-role-1"]
        role_2 = request.form["select-role-2"]
        region = request.form["select-region"]
        if users.query.filter_by(riot_id=riotid).first():
            flash("Этот Riot ID уже привязан у другому аккаунту")
            return redirect(url_for("connect"))
        elif re.match(r'[^#]{3,16}#[^#]{3,5}', riotid):
            name, tag = riotid.split('#')
            puuid = riot_funcs.get_account_puuid(name, tag, keys.riot_api_key)
            print(puuid)
            try:
                icon_id = str(riot_funcs.get_summoner_info_by_puuid(region, puuid, keys.riot_api_key)['profileIconId'])
            except:
                flash("Выбран неправильный сервер")
                return redirect(url_for("connect"))
            # if icon_id == str(session["icon_number"]):
            if True:
                flash("Успешная регистрация")
                user = db.session.execute(db.select(users).filter_by(username=current_user.username)).scalar_one()
                user.riot_id = riotid
                user.role_1 = role_1
                user.role_2 = role_2
                user.region = region
                db.session.commit()
                return redirect(url_for("profile"))
        return redirect(url_for("profile"))

    else:

        session["icon_number"] = random.randint(1,29)
        print(session["icon_number"])
        return render_template("connect.html", number=session["icon_number"])


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
