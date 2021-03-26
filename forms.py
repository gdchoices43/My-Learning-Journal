from flask_wtf import Form
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo
from wtforms import TextAreaField, StringField,  DateField, IntegerField, PasswordField

from models import User


class Entry(Form):
    title = StringField("Title:", validators=[DataRequired()])
    date = DateField("Date:(format-MM/DD/YYYY)", format="%m/%d/%Y", validators=[DataRequired()])
    est_time = IntegerField("Time Spent:(in hours)", validators=[DataRequired()])
    i_learned = TextAreaField("What I Learned:", validators=[DataRequired()])
    resources = TextAreaField("Resources To Remember:", validators=[DataRequired()])


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("User with that name already exists!")


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("User with that email already exists!")


class SignUp(Form):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Regexp(
                r"^[a-zA-Z0-9_]+$",
                message=("Username should be one word, consisting of letters,"
                         "numbers, and underscores only!")
            ),
            name_exists
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(),
            EqualTo("password2", message="Passwords must match!")
        ]
    )
    password2 = PasswordField(
        "Confirm Password",
        validators=[DataRequired()]
    )


class Login(Form):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
