from flaskie_app import app
from forms import NewTodo
import flask
import requests
from flask import request, redirect, url_for
from mnworkie_todo import JsonSerDe
import json

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
    url = f'http://localhost:8000/todos/{index}'
    data = requests.get(url)
    return data.text
