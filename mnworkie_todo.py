import hug
import json
import uuid
from db_control import ConnectionDB

conn = ConnectionDB.create_conn('updated_mnatabase.db')
class SerDe:
    @classmethod
    def load(cls):pass
    @classmethod
    def save(cls, todo):pass

class DBSerDe(SerDe):
    @classmethod
    def load(cls):
        return ConnectionDB.show_todos(conn)

    @classmethod
    def save(cls, todo):
        return ConnectionDB.upsert_todo(conn, todo_parameters=todo)



class JsonSerDe(SerDe):
    @classmethod
    def load(cls):
        with open('mnworkie_json', 'r') as file:
            return json.load(file)

    @classmethod
    def save(cls, todo):
        with open('mnworkie_json', 'w') as file:
            return json.dump(todo, file, indent=4)



@hug.get('/todos')
def todo(user_id: int):
   all_todos = ConnectionDB.show_todos(conn, user_id)
   return all_todos


@hug.get('/todos/{todo_id}')
def view_single_td(todo_id: int):
    return ConnectionDB.show_single_todo(conn, todo_id)



@hug.put('/todos')
def todo_update(name, description, done: int, id, user_id):
    todo_parameters = (name, description, done, id, user_id)
    DBSerDe.save(todo_parameters)
    return hug.redirect.see_other('/todos')

@hug.post('/todos')
def new_todo_post(name, description=None, done: bool=False):
    new_todo(name, description, done)
    return hug.redirect.see_other('/todos')

@hug.delete('/todos/{todo_id}')
def todo_delete(index: str):
    load_todo = JsonSerDe.load()
    del load_todo[index]
    JsonSerDe.save(load_todo)
    return load_todo


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


