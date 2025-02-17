from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from flask import current_app as app
from . import db
from .forms import LoginForm, RegisterForm, ConnectForm
from .models import Users, RiotAccountInfoUser, Tournaments
from .services import register_user, connect_riot_account
from .utils import get_user_by_email_or_username
import random

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
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
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    form = RegisterForm()
    if form.validate_on_submit():
        return register_user(form)
    return render_template("register.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("username", None)
    return redirect(url_for("home"))


@app.route("/profile")
@login_required
def profile():
    tournament_list = Tournaments.query.all()
    return render_template("profile.html", tournament_list=tournament_list, user=current_user)


@app.route("/connect", methods=["GET", "POST"])
@login_required
def connect():
    form = ConnectForm()
    if form.validate_on_submit():
        return connect_riot_account(form)
    else:
        session["icon_number"] = str(random.randint(1, 28))
        return render_template("connect.html", form=form, number=session["icon_number"])