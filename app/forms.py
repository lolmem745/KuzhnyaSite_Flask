from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

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


class ConnectForm(FlaskForm):
    riotid = StringField('Riot ID', validators=[DataRequired()], render_kw={"placeholder": "Riot ID"})
    select_role_1 = SelectField('Role 1', choices=[('top', 'Топ'), ('jgl', 'Лес'), ('mid', 'Мид'), ('sup', 'Саппорт'), ('bot', 'Бот')], validators=[DataRequired()])
    select_role_2 = SelectField('Role 2', choices=[('top', 'Топ'), ('jgl', 'Лес'), ('mid', 'Мид'), ('sup', 'Саппорт'), ('bot', 'Бот')], validators=[DataRequired()])
    select_region = SelectField('Region', choices=[('euw1', 'EUW'), ('ru', 'RU')], validators=[DataRequired()])
    submit = SubmitField('Connect')