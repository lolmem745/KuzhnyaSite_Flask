from flask import flash, redirect, url_for
from flask_login import current_user
from .models import Users, RiotAccountInfoUser, db, Tournaments, Games
from . import utils
import keys
import re
from werkzeug.security import generate_password_hash

def register_user(form):
    email = form.email.data
    username = form.username.data
    password = form.password.data
    found_user = utils.get_user_by_email_or_username(email) or utils.get_user_by_email_or_username(username)
    if found_user:
        flash("Пользователь с таким ником/почтой уже зарегестрирован")
        return redirect(url_for("register"))
    else:
        user = Users(username, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Успешная регистрация")
        return redirect(url_for("home"))

def connect_riot_account(form):
    riotid = utils.clean_input(form.riotid.data)
    role_1 = form.select_role_1.data
    role_2 = form.select_role_2.data
    region = form.select_region.data
    if RiotAccountInfoUser.query.filter_by(riot_id=riotid).first():
        flash("Этот Riot ID уже привязан к другому аккаунту")
        return redirect(url_for("connect"))
    elif re.match(r'[^#]{3,16}#[^#]{3,5}', riotid):
        name, tag = riotid.split('#')
        puuid = utils.get_account_puuid(name, tag, keys.riot_api_key)

        try:
            icon_id = str(utils.get_summoner_info_by_puuid(region, puuid, keys.riot_api_key)['profileIconId'])
        except:
            flash("Выбран неправильный сервер")
            return redirect(url_for("connect"))
        flash("Успешная регистрация")
        user = current_user
        riot_info = RiotAccountInfoUser(
            user_id=user.id,
            riot_id=riotid,
            role_1=role_1,
            role_2=role_2,
            region=region,
            icon_id=icon_id
        )
        db.session.add(riot_info)
        db.session.commit()
        return redirect(url_for("profile"))
    return redirect(url_for("profile"))

def add_tournament(form):
    tournament = Tournaments(tournament_name=form.tournament_name.data)
    db.session.add(tournament)
    db.session.commit()
    return tournament

def add_game(form):
    game = Games(
        game_name=form.game_name.data,
        game_time=form.game_time.data,
        tournament_id=form.tournament_id.data
    )
    db.session.add(game)
    db.session.commit()
    return game

def edit_user(form):
    user = Users.query.get(form.user_id.data)
    if user:
        if form.username.data:
            user.username = form.username.data
        if form.email.data:
            user.email = form.email.data
        if form.password.data:
            user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        return user
    return None