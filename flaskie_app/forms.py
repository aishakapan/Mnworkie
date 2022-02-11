from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, validators
from wtforms.validators import DataRequired, Optional


class NewTodo(FlaskForm):
    name = StringField('Write a new todo here!', validators=[DataRequired()])
    description = StringField('Add a description.', validators=[Optional()])
    done = BooleanField('Done status.', validators=[Optional()])
    submit = SubmitField('Submit.')

class Login(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = StringField('Password', validators=[DataRequired()])

class Signup(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25,
                                                          message=('Username should contain at least 4 characters.'))])
    password = StringField('Password', validators=[DataRequired()])