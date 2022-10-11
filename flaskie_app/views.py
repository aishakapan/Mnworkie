import logging
from functools import wraps
import hashlib
import base64
from werkzeug.security import generate_password_hash, check_password_hash
from forms import NewTodo, Login, Signup
import flask
import requests
from flask import request, redirect, url_for, flash, session
import json
from models import Users, Todos
from app import create_app
from create_db import create_db
from db.db_control import ConnectionDB

logging.basicConfig(level=logging.DEBUG)

db = create_db()
app = create_app()



# this function is not really used anymore, since
# requests library provides a separate authorization functionality
def generate_authorization_headers(username, password):

    encrypted_pword = generate_password_hash(password, method='sha256')
    credentials = f'{username}:{encrypted_pword}'
    encoded_credentials = base64.b64encode(credentials.encode('UTF-8')).decode('ASCII')
    authorization_data = {"Authorization": f"Basic {encoded_credentials}"}
    return authorization_data

# currently used python built-in functions hashing
def hashing_256(password):

    encoded = password.encode()
    result = hashlib.sha256(encoded)

    return result.hexdigest()


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'auth' not in session:
            return redirect(url_for('login', _method="GET"))
        return func(*args, **kwargs)
    return wrapper


def get_all_todos(username, encrypted_pword):

    url = url_for('todos', _external=True)
    view = requests.get(url, auth=(username, encrypted_pword))

    return view.json()


def get_single_todo(todo_id):

    url = f"{url_for('todos', _external=True)}/{todo_id}"
    view = requests.get(url, auth=session['auth'])
    view.raise_for_status()

    return view.json()

def signup_db(username, password):
    user = (username, password)
    conn = ConnectionDB.create_conn('mnworkie.db')
    ConnectionDB.add_user(conn, user)
    return True

def login_db(username, password):
    conn = ConnectionDB.create_conn('mnworkie.db')
    exists = ConnectionDB.check_user(conn, username, password)
    return exists

def new_td_db():
    pass

def patch_db():
    pass

def delete_db():
    pass

def get_todos_db():
    pass

def get_one_todo_db():
    pass


@app.route('/')
def mnworkie():
    return flask.render_template('landing_page.html')

@app.route("/todos")
@login_required
def todos():

    data = get_todos_db()

    for todo in data:
        link = url_for(single_td.__name__, todo_id=todo['id'])
        todo['link'] = link

    html = flask.render_template('mnoverview.html', todos=data)

    return html


@app.route("/todos/<todo_id>")
@login_required
def single_td(todo_id):

    data = get_one_todo_db(todo_id)
    html = flask.render_template('single_view.html', todos=data, todo_id=todo_id)

    return html


@app.route("/todos/<todo_id>", methods=['PATCH'])
@login_required
def patch_td(todo_id):
    patch_td(todo_id)
    flash('Todo modified successfully.')
    return redirect(url_for('todos'))


@app.route("/todos/<todo_id>", methods=['DELETE'])
@login_required
def delete_td(todo_id):
    delete_db(todo_id)
    flash('Todo deleted successfully.')
    return redirect(url_for('todos'))


@app.route("/newtd", methods=['GET', 'POST'])
@login_required
def new_td():

    if request.method == 'POST':
        new_td = NewTodo(request.form)
        url = url_for('todos')
        todo = {'name': new_td.name.data,
                'description': new_td.description.data,
                'done': True if new_td.done.data == 'y' else ''}
        new_td.validate_on_submit()

        new_td_db()
        # logging.info(res.content, stack_info=True)
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

    print('SESS: ', session)
    username = request.form.get('username')
    password = request.form.get('password')
    encrypted_pword = hashing_256(password)


    # url = url_for('signup', _external=True)
    # data = {'username': username,
    #         'password': encrypted_pword}


    # response.raise_for_status()


    # if response.text == 'User already exists!':
    #     return response.text
    # else:
    response = signup_db(username, encrypted_pword)
    if response:
        flask.flash('Signed up successfully.')
        return redirect(url_for("login"))



@app.route("/login", methods=['GET'])
def login():

    form = Login()
    flask.flash('You need to be logged in to view and edit todos.')
    return flask.render_template('login.html', form=form)



@app.route("/login", methods=['POST'])
def login_post():

    username = request.form.get('username')
    password = request.form.get('password')
    # print(password)
    # print(request.form)
    # url = url_for('login', _external=True)
    encrypted_pword = hashing_256(password)
    # print(encrypted_pword)
    response = login_db(username, encrypted_pword)

    if response:
        flask.flash('Logged in successfully.')
        session['auth'] = (username, encrypted_pword)
        return redirect(url_for('todos', _method='GET'))

    elif not response:
        flask.flash('Wrong credentials. Please try again.')
        return redirect(url_for('login'))
    # else:
    #     response.raise_for_status()



@app.route('/logout')
def logout():
    session.pop('auth', None)
    return redirect(url_for('/'))