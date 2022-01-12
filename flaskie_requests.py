import requests
import json
from mnworkie_todo import JsonSerDe, loading_short_dict
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Optional
from wtforms import StringField, SubmitField, BooleanField
from flask import Flask, request, redirect, url_for
import flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

class NewTodo(FlaskForm):
    name = StringField('Write a new todo here!', validators=[DataRequired()])
    description = StringField('Add a description.', validators=[Optional()])
    done = BooleanField('Done status.', validators=[Optional()])
    submit = SubmitField('Submit.')


def get_todo():
    url = 'http://localhost:8000/todo'
    view = requests.get(url)
    return view.content


@app.route("/todos")
def todos():
    data = get_todo()
    html = flask.render_template('mnoverview.html', todos = json.loads(data))
    return html

@app.route("/newtd", methods = ['GET'])
def new_td():
    new_td = NewTodo()
    if request.method == 'GET':
        return flask.render_template('new_todo.html', form=new_td)
    return redirect(url_for('todos'))
# FIXME make a single view with descriptions

@app.route("/todos/<index>")
def single_td(index):
    url = f'http://localhost:8000/todo/{index}'
    data = requests.get(url)
    return data.text


def update_todo(name, done):
    url = 'http://localhost:8000/todo'
    change = {"name": name, "done": done}
    updating = requests.put(url, json=change, allow_redirects=True)
    return updating.status_code



def delete_todo(index):
    url = f'http://localhost:8000/todo/{index}'
    load_json = JsonSerDe.load()
    change = load_json[index]
    deleting = requests.delete(url, json=change)
    return deleting.status_code


