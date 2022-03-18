import logging
import hashlib
import base64
from werkzeug.security import generate_password_hash, check_password_hash
from flaskie_app.forms import NewTodo, Login, Signup
import flask
import requests
from flask import request, redirect, url_for, flash, session
import json
from flask_login import login_required
from .models import Users, Todos
from . import db, app

logging.basicConfig(level=logging.DEBUG)

def get_all_todos(username, encrypted_pword):
    url = f'http://localhost:8000/todos'
    view = requests.get(url, auth=(username, encrypted_pword))
    return view.json()


def get_single_todo(user_id, todo_id):
    url = f'http://localhost:8000/todos/{user_id}/{todo_id}'
    view = requests.get(url)
    return view.content

@login_required
@app.route("/todos")
def todos():
    print(session)
    data = get_all_todos(*session['auth'])
    print(data)

    html = flask.render_template('mnoverview.html', todos=data)

    return html

@login_required
@app.route("/todos/<todo_id>")
def single_td(todo_id):

    data = get_single_todo(session['user_id'], todo_id)
    html = flask.render_template('mnoverview.html', todos=data)

    return html


@app.route("/newtd", methods=['GET', 'POST'])
def new_td():

    if request.method == 'POST':
        new_td = NewTodo(request.form)
        new_td.validate_on_submit()
        url = f'http://localhost:8000/todos'
        todo = {'name': new_td.name.data,
                'description': new_td.description.data,
                'done': new_td.done.data == 'y'}
        print("This is form stuff:", request.form)

        res = requests.post(url, data=todo, auth=session['auth'])
        print(res.status_code)
        logging.info(res.text, stack_info=True)
        return redirect(url_for('todos'))

    if request.method == 'GET':
        new_td = NewTodo()
        return flask.render_template('new_todo.html', form=new_td, user_id=1)




@app.route("/signup", methods=['GET'])
def signup():
    form = Signup()
    return flask.render_template('signup.html', form=form)


@app.route("/signup", methods=['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')

    form = Signup(username=username, password=password)
    user = Users.query.filter_by(username=username).first()

    if user:
        flash('Username already exists! Please enter another one.')
        return redirect(url_for("signup"))

    new_user = Users(username=username,
                     password=generate_password_hash(password, method='sha256'))
    validate = form.validate_on_submit()



    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("login"))


# this function is not really used anymore, since
# requests library provides a separate authorization functionality
def generate_authorization_headers(username, password):
    encrypted_pword = generate_password_hash(password, method='sha256')
    credentials = f'{username}:{encrypted_pword}'
    encoded_credentials = base64.b64encode(credentials.encode('UTF-8')).decode('ASCII')
    authorization_data = {"Authorization": f"Basic {encoded_credentials}"}
    return authorization_data

def hashing_256(password):
    encoded = password.encode()
    result = hashlib.sha256(encoded)
    return result.hexdigest()


@app.route("/login", methods=['GET'])
def login():
    form = Login()
    return flask.render_template('login.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login_post():

    username = request.form.get('username')
    password = request.form.get('password')
    encrypted_pword = hashing_256(password)


    # authorization_headers = generate_authorization_headers(username, password)
    # print(authorization_headers)
    url = f'http://localhost:8000/login'
    response = requests.post(url, auth=(username, encrypted_pword))


    response.raise_for_status()
    flask.flash('Logged in successfully.')
    session['auth'] = (username, encrypted_pword)

    return redirect(url_for('todos'))




@app.route('/logout')
def logout():
    session.pop('auth', None)
    return 'You have been logged out.'
