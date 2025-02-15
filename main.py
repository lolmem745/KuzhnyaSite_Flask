from flask import Flask, render_template, redirect, url_for, request, flash, session
from datetime import timedelta, datetime, time
from flask_sqlalchemy import SQLAlchemy
import re
import random

from sqlalchemy.orm import backref

import riot_funcs
import keys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = keys.APP_SECRET_KEY
app.permanent_session_lifetime = timedelta(days=1)
app.app_context().push()
db = SQLAlchemy(app)


def clean_input (input_string):
    # Удаляем невидимые символы Unicode, такие как ZERO WIDTH SPACE
    cleaned = re.sub(r'[\u200b\u200c\u200d\u2060\u2061]', '', input_string)
    # Убираем любые другие неотображаемые символы
    cleaned = ''. join(c for c in cleaned if c.isprintable())
    return cleaned.strip()

class users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(30))
    password = db.Column(db.String(25))
    riot_user = db.relationship("riot_account_info_user", backref=backref("users", uselist=False))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


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

    def __init__(self, tournament_name, game_name, game_time):
        self.tournament_name = tournament_name
        self.game_name = game_name
        self.game_time = game_time


def get_user_tournaments(user_id):
    tournament_list = tournaments.query.all()
    return tournament_list


user = users.query.filter_by(username='memlol745').first()
print(user.riot_user)
x = riot_account_info_user.query.first()
print(x)




@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        password = request.form["password"]
        found_user = users.query.filter_by(email=username).first()
        if found_user is None:
            found_user = users.query.filter_by(username=username).first()
        if found_user:
            if found_user.username == username or found_user.email == username:
                if found_user.password == password:
                    session["email"] = found_user.email
                    session["username"] = found_user.username
                else:
                    flash("Неверный пароль")
                    return redirect(url_for("login"))
            return redirect(url_for("home"))
        else:
            flash("Пользователя с такими данными не найдено")
            return redirect(url_for("login"))
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        session.permanent = True

        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        password_repeat = request.form["password-repeat"]
        found_user = users.query.filter_by(email=username).first()
        if found_user is None:
            found_user = users.query.filter_by(username=username).first()
        if found_user:
            flash("Пользователь с таким ником/почтой уже зарегестрирован")
            return redirect(url_for("register"))
        elif not re.fullmatch(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
            flash("Слабый пароль")
            return redirect(url_for("register"))
        elif not password == password_repeat:
            flash("Пароли не совпадают")
            return redirect(url_for("register"))
        else:
            session["email"] = email
            session["username"] = username
            user = users(username, email, password)
            db.session.add(user)
            db.session.commit()
            flash("Успешная регистрация")
            return redirect(url_for("home"))


    else:
        try:
            if session["username"]:
                flash("Вы уже зарегестрированы.")
                return redirect(url_for("home"))

        except KeyError:
            return render_template("register.html")
        else:
            if session["username"]:
                flash("Вы уже зарегестрированы.")
                return redirect(url_for("home"))
            return render_template("register.html")




@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    if "email" in session:
        session.pop("email")
    return redirect(url_for("home"))


@app.route("/profile")
def profile():
    tournament_list = get_user_tournaments(1)
    if session["username"]:
        user = users.query.filter_by(username=session["username"]).first()

    return render_template("profile.html", tournament_list=tournament_list, user=user)


@app.route("/connect", methods = ["GET", "POST"])
def connect():
    if request.method == "POST":
        riotid = clean_input(request.form["riotid"])
        role_1 = request.form["select-role-1"]
        role_2 = request.form["select-role-2"]
        region = request.form["select-region"]
        if users.query.filter_by(riot_id= riotid).first():
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
                user = db.session.execute(db.select(users).filter_by(username=session["username"])).scalar_one()
                user.riot_id = riotid
                user.role_1 = role_1
                user.role_2 = role_2
                user.region = region
                db.session.commit()
                return redirect(url_for("profile"))
        return redirect(url_for("profile"))

    else:
        icon_list = [7, 9, 18, 20, 23]
        session["icon_number"] = random.choice(icon_list)
        print(session["icon_number"])
        return render_template("connect.html", number=session["icon_number"])


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
