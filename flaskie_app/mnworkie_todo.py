import logging

import hug
import json
import uuid
from db.db_control import ConnectionDB

logging.basicConfig(level=logging.DEBUG)

class SerDe:
    @classmethod
    def load(cls, user_id):pass
    @classmethod
    def save(cls, todo):pass



class DBSerDe(SerDe):
    conn = ConnectionDB.create_conn('/home/morkovka/PycharmProjects/Mnworkie/flaskie_app/updated_mnatabase.db')

    @classmethod
    def load(cls, user_id):
        return ConnectionDB.show_todos(cls.conn, user_id)

    @classmethod
    def save(cls, todo):
        return ConnectionDB.upsert_todo(cls.conn, todo_parameters=todo)

    @classmethod
    def add_user(cls, user):
        return ConnectionDB.add_user(cls.conn, user)

    @classmethod
    def show_single(cls, todo_id):
        return ConnectionDB.show_single_todo(cls.conn, todo_id)

    @classmethod
    def post(cls, todo):
        return ConnectionDB.create_todo(cls.conn, todo)

    @classmethod
    def delete(cls):
        return ConnectionDB.delete_todo(cls.conn, id)



class JsonSerDe(SerDe):
    @classmethod
    def load(cls):
        with open('../mnworkie_json', 'r') as file:
            return json.load(file)

    @classmethod
    def save(cls, todo):
        with open('../mnworkie_json', 'w') as file:
            return json.dump(todo, file, indent=4)


def verify(username, password):
    id = ConnectionDB.check_user(username, password)
    if id == None:
        return False
    else:
        return id

# maybe just post
@hug.get_post('/signup')
def signup(username, password):
    user = (username, password)
    # i.e. if a user does not exist (cannot find his id) then register
    if not verify(*user):
        DBSerDe.add_user(user)
        return hug.redirect.see_other('/login')
    else:
        return 'User already exists!'

@hug.get_post('/login', requires=hug.authentication.basic(verify))
def login(user:hug.directives.user):
     return user


@hug.get('/todos', requires=hug.authentication.basic(verify))
def todo(user:hug.directives.user):
    todos = DBSerDe.load(user_id=user[0])

    return todos


@hug.get('/todos/{todo_id}', requires=hug.authentication.basic(verify))
def view_single_td(todo_id: int):
    return DBSerDe.show_single(todo_id)


@hug.put('/todos', requires=hug.authentication.basic(verify))
def todo_update(name, description, done: int, id, user:hug.directives.user):
    todo_parameters = (name, description, user, done, id)
    DBSerDe.save(todo_parameters)
    return hug.redirect.see_other('/todos')


@hug.post('/todos', requires=hug.authentication.basic(verify))
def new_todo_post(name, user:hug.directives.user, description=None, done: bool=False):
    new_todo = (name, description, user[0], done)
    DBSerDe.post(new_todo)
    return hug.redirect.see_other('/todos')



@hug.delete('/todos/{todo_id}')
def todo_delete(todo_id: str):
    DBSerDe.delete(todo_id)
    return hug.redirect.see_other('/todos')



@hug.cli()
def new_todo_cli(name, description, done: bool=False):
    new_todo(name, description, done)
    return



# @hug.get('/user/{user_id}/todos')
def todo_user(user_id: int):
    input_dict = loading_short_dict()
    output_dict = {k:v for k,v in input_dict.items() if v['user_id'] == user_id}
    return output_dict

# @hug.get('/todos/{index}')
def view_single_td_json(index: str):
    load_todo = JsonSerDe.load()
    return load_todo[f"{index}"]


def loading_short_dict():
    todo_dict = JsonSerDe.load()

    new_todo_dict = todo_dict.copy()
    for outer_k, outer_v in new_todo_dict.items():
        for inner_k in list(outer_v):
            if inner_k == "description":
               outer_v.pop(inner_k)
    return new_todo_dict


def new_todo(name, description, done: bool=False):
    load_todo = JsonSerDe.load()
    new_dict = {'user_id': 1,
                'name': name,
                'done': done,
                'description': description}
    index = str(uuid.uuid4())
    load_todo[index] = new_dict
    JsonSerDe.save(load_todo)




# updating an EXISTING to-do
# @hug.put('/todos')
def todo_update(index: str, name, description, done: bool):
    load_todo = JsonSerDe.load()
    new_dict = {'user_id': 1,
                'name': name,
                'done': done,
                'description': description}
    load_todo[index] = new_dict
    JsonSerDe.save(load_todo)
    return load_todo


# @hug.post('/todos')
def new_todo_post(name, description=None, done: bool=False):
    new_todo(name, description, done)
    return hug.redirect.see_other('/todos')
#
# @hug.delete('/todos/{todo_id}')
def todo_delete(index: str):
    load_todo = JsonSerDe.load()
    del load_todo[index]
    JsonSerDe.save(load_todo)
    return load_todo
