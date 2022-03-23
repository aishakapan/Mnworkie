from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators, SelectField
from wtforms.validators import DataRequired, Optional



class NewTodo(FlaskForm):
    name = StringField('Write a new todo here!', validators=[DataRequired()])
    description = StringField('Add a description.', validators=[Optional()])
    done = SelectField('Done status', choices=[('y', 'true'), ('', 'false')])
    # done = BooleanField('Done status.', validators=[Optional()])
    submit = SubmitField('Submit')

class Login(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class Signup(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25,
                                                          message=('Username should contain at least 4 characters.'))])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Signup')