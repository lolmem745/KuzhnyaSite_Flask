from flask import flash, redirect, url_for
from flask_login import current_user
from .models import Users, RiotAccountInfoUser, db, Tournaments, Games, Teams
from . import utils
import keys
import re
from werkzeug.security import generate_password_hash
import uuid
from .utils import get_summoner_info_by_puuid

def register_user(form):
    email = form.email.data
    username = form.username.data
    password = form.password.data
    found_user = utils.get_user_by_email_or_username(email) or utils.get_user_by_email_or_username(username)
    if found_user:
        flash("Пользователь с таким ником/почтой уже зарегестрирован")
        return redirect(url_for("routes.register"))
    else:
        user = Users(username, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Успешная регистрация")
        return redirect(url_for("routes.home"))

def connect_riot_account(form):
    riotid = utils.clean_input(form.riotid.data)
    role_1 = form.select_role_1.data
    role_2 = form.select_role_2.data
    region = form.select_region.data
    if RiotAccountInfoUser.query.filter_by(riot_id=riotid).first():
        flash("Этот Riot ID уже привязан к другому аккаунту")
        return redirect(url_for("routes.connect"))
    elif re.match(r'[^#]{3,16}#[^#]{3,5}', riotid):
        name, tag = riotid.split('#')
        puuid = utils.get_account_puuid(name, tag, keys.riot_api_key)

        try:
            icon_id = str(utils.get_summoner_info_by_puuid(region, puuid, keys.riot_api_key)['profileIconId'])
        except:
            flash("Выбран неправильный сервер")
            return redirect(url_for("routes.connect"))
        flash("Успешная регистрация")
        user = current_user
        riot_info = RiotAccountInfoUser(
            user_id=user.id,
            riot_id=riotid,
            riot_puuid=puuid,
            role_1=role_1,
            role_2=role_2,
            region=region,
            icon_id=icon_id
        )
        db.session.add(riot_info)
        db.session.commit()
        return redirect(url_for("routes.profile"))
    return redirect(url_for("routes.profile"))

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

def add_team(form):
    team = Teams(
        team_name=form.team_name.data,
        captain_id=form.captain_id.data,
        join_token=str(uuid.uuid4())
    )
    
    db.session.add(team)
    db.session.commit()

    user = Users.query.get(form.captain_id.data)
    user.team_id = team.id
    db.session.commit()
    
    return team

def edit_team(form):
    team = Teams.query.get(form.team_name.data)
    if team:
        team.team_name = form.new_team_name.data
        team.captain_id = form.captain_id.data
        db.session.commit()
        return team
    return None

def generate_team_link(team_id, user_id):
    team = Teams.query.get(team_id)
    if not team or team.captain_id != user_id:
        return {"error": "You are not the captain of this team."}, 403
    link = url_for('routes.join_team_by_token_route', token=team.join_token, _external=True)
    return {"link": link}, 200

def join_team_by_token(token, user_id):
    team = Teams.query.filter_by(join_token=token).first()
    if not team:
        return {"error": "Team not found."}, 404
    if len(team.members) >= 5:
        return {"error": "Team is full."}, 403
    user = Users.query.get(user_id)
    user.team_id = team.id
    db.session.commit()
    return {"message": "Joined team successfully."}, 200

def refresh_riot_account_info(user):
    if user.riot_user:
        try:
            summoner_info = get_summoner_info_by_puuid(user.riot_user.region, user.riot_user.riot_puuid, keys.riot_api_key)
            user.riot_user.icon_id = summoner_info['profileIconId']
            db.session.commit()
        except Exception as e:
            print(f"Error refreshing Riot account info: {e}")