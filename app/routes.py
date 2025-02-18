from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from flask import current_app as app
from . import db
from .forms import LoginForm, RegisterForm, ConnectForm, TournamentForm, GameForm, EditUserForm
from .models import Users, RiotAccountInfoUser, Tournaments, Games
from .services import register_user, connect_riot_account, add_tournament, add_game, edit_user
from .utils import get_user_by_email_or_username, admin_required
import random
from werkzeug.security import generate_password_hash



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
def logout():
    logout_user()
    session.pop("username", None)
    return redirect(url_for("home"))


@app.route("/profile")
@login_required
def profile():
    game_list = current_user.games
    return render_template("profile.html", game_list=game_list, user=current_user)


@app.route("/connect", methods=["GET", "POST"])
@login_required
def connect():
    form = ConnectForm()
    if form.validate_on_submit():
        return connect_riot_account(form)
    else:
        session["icon_number"] = str(random.randint(1, 28))
        return render_template("connect.html", form=form, number=session["icon_number"])

@app.route("/tournaments")
def get_tournaments():
    tournaments = Tournaments.query.all()
    return render_template("tournaments.html", tournament_list=tournaments)


@app.route("/tournaments/<int:id>")
def get_tournament_by_id(id):
    tournament = Tournaments.query.filter_by(id=id).first()
    return render_template("tournament_page.html", tournament=tournament)

@app.route("/admin", methods=["GET", "POST"])
@admin_required
def admin():
    tournament_form = TournamentForm()
    game_form = GameForm()
    edit_user_form = EditUserForm()

    game_form.tournament_id.choices = [(t.id, t.tournament_name) for t in Tournaments.query.all()]
    edit_user_form.user_id.choices = [(u.id, u.username) for u in Users.query.all()]

    if tournament_form.validate_on_submit():
        add_tournament(tournament_form)
        flash("Tournament added successfully.")
        return redirect(url_for("admin"))

    if game_form.validate_on_submit():
        add_game(game_form)
        flash("Game added successfully.")
        return redirect(url_for("admin"))

    if edit_user_form.validate_on_submit():
        user = edit_user(edit_user_form)
        if user:
            flash("User info updated successfully.")
        else:
            flash("User not found.")
        return redirect(url_for("admin"))
    
    users = Users.query.all()
    tournaments = Tournaments.query.all()
    return render_template("admin.html", tournament_form=tournament_form, game_form=game_form, edit_user_form=edit_user_form, users=users, tournaments=tournaments)