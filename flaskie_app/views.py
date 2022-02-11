import flask_login

from flaskie_app import app
from flaskie_app.forms import NewTodo, Login
import flask
import requests
from flask import request, redirect, url_for
import json
from flask_login import LoginManager, UserMixin


login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    pass

def get_all_todos(user_id):
    url = f'http://localhost:8000/todos/{user_id}'
    view = requests.get(url)
    return view.content

def get_single_todo(user_id, todo_id):
    url = f'http://localhost:8000/todos/{user_id}/{todo_id}'
    view = requests.get(url)
    return view.content

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/todos")
def todos():
    data = get_all_todos(1)
    html = flask.render_template('mnoverview.html', todos = json.loads(data))
    return html

@app.route("/newtd", methods = ['GET', 'POST'])
def new_td():

    if request.method == 'POST':
        new_td = NewTodo(request.form)
        user_id = request.args.get('user_id')
        url = f'http://localhost:8000/todos/{user_id}'
        todo = {'name': new_td.name.data,
                'description': new_td.description.data,
                'done': new_td.done.data}
        requests.post(url, data=todo)
        return redirect(url_for('todos'))

    if request.method == 'GET':
        new_td = NewTodo()
        return flask.render_template('new_todo.html', form=new_td, user_id = 1)


@app.route("/todos/<todo_id>")
def single_td(todo_id):
    user_id = request.args.get('user_id')

    data = get_single_todo(user_id, todo_id)
    html = flask.render_template('mnoverview.html', todos=json.loads(data))
    return html
@app.route("/signup", methods=['GET', 'POST'])
def signup():
   return redirect(url_for("login"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    user = User()
    form = Login()
    if form.validate_on_submit():
        flask_login.login_user(user)
        flask.flash('Logged in successfully.')

        return redirect(url_for('todos'))
    return flask.render_template('login.html', form=form)





