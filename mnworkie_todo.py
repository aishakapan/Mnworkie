import hug
import json
import uuid
from db_control import ConnectionDB


class SerDe:
    @classmethod
    def load(self):pass
    @classmethod
    def save(self, todo):pass


class JsonSerDe(SerDe):
    @classmethod
    def load(cls):
        with open('mnworkie_json', 'r') as file:
            return json.load(file)

    @classmethod
    def save(cls, todo):
        with open('mnworkie_json', 'w') as file:
            return json.dump(todo, file, indent=4)

conn = ConnectionDB.create_conn('mnatabase.db')
rows_names = ConnectionDB.fetch_rows(conn)
data_entries = ConnectionDB.show_todos(conn)

@hug.get('/todo')
def todo():
   # full_data = list(zip(rows_names, *data_entries))
   return data_entries

@hug.get('/todo/user/{user_id}')
def todo_user(user_id: int):
    input_dict = loading_short_dict()
    output_dict = {k:v for k,v in input_dict.items() if v['user_id'] == user_id}
    return output_dict

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


# viewing a single to-do with description at a certain endpoint
@hug.get('/todo/{index}')
def view_single_td(index: str):
    load_todo = JsonSerDe.load()
    return load_todo[f"{index}"]

# updating an EXISTING to-do
@hug.put('/todo')
def todo_update(index: str, name, description, done: bool):
    load_todo = JsonSerDe.load()
    new_dict = {'user_id': 1,
                'name': name,
                'done': done,
                'description': description}
    load_todo[index] = new_dict
    JsonSerDe.save(load_todo)
    return load_todo



# posting a NEW to-do
@hug.post('/todo')
def new_todo_post(name, description, done: bool=False):
    new_todo(name, description, done)
    return hug.redirect.see_other('/todo')

# deleting to-do at a specified index
@hug.delete('/todo/{index}')
def todo_delete(index: str):
    load_todo = JsonSerDe.load()
    del load_todo[index]
    JsonSerDe.save(load_todo)
    return load_todo

# using hug from command line interface
@hug.cli()
def new_todo_cli(name, description, done: bool=False):
    new_todo(name, description, done)
    return

