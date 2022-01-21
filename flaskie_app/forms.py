from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional


class NewTodo(FlaskForm):
    name = StringField('Write a new todo here!', validators=[DataRequired()])
    description = StringField('Add a description.', validators=[Optional()])
    done = BooleanField('Done status.', validators=[Optional()])
    submit = SubmitField('Submit.')