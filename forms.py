from flask_wtf import Form
from wtforms.validators import DataRequired
from wtforms import TextAreaField, StringField,  DateField, IntegerField


class EntryForm(Form):
    title = StringField("Title:", validators=[DataRequired()])
    date = DateField("Date:(format-MM/DD/YYYY)", format="%m/%d/%Y", validators=[DataRequired()])
    time = IntegerField("Time Spent:(in hours)", validators=[DataRequired()])
    i_learned = TextAreaField("What I Learned:", validators=[DataRequired()])
    resources = TextAreaField("Resources To Remember:", validators=[DataRequired()])
