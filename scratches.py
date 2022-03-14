import hashlib
from db.db_control import ConnectionDB

database = r'C:\Users\aisha\PycharmProjects\Mnworkie\mnatabase.db'
conn = ConnectionDB.create_conn(database)

#
# def fetch_rows():
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()
#     cur.execute('select * from todos')
#     rows = cur.fetchone()
#     return rows.keys()
#
# print(fetch_rows())
# conn = ConnectionDB.create_conn('mnatabase.db')
# data = list(ConnectionDB.show_todos(conn))
# print(data)
# rows = fetch_rows()
# combined = list(zip(rows, *data))
# print(combined)
#
# sql_create_users = """CREATE TABLE IF NOT EXISTS users(
#                                                     id integer PRIMARY KEY,
#                                                     username text NOT NULL,
#                                                     password NOT NULL
#                                                     );"""
# sql_create_todos = """CREATE TABLE IF NOT EXISTS todos(
#                                                     id integer PRIMARY KEY,
#                                                     name text NOT NULL,
#                                                     description text,
#                                                     done integer NOT NULL,
#                                                     user_id integer NOT NULL,
#                                                     FOREIGN KEY(user_id) REFERENCES users(id)
#                                                     );"""
# if conn is not None:
#     ConnectionDB.create_table(conn, sql_create_users)
#     ConnectionDB.create_table(conn, sql_create_todos)
#
#
# def new_td():
#     with app.app_context():
#         new_td = NewTodo()
#         user_id = request.args.get('user_id')
#         url = f'http://localhost:8000/todos/{user_id}'
#         if request.method == 'POST':
#             r = requests.post(url, params=request.args)
#             print(r.status_code)
#
# new_td()

def hashing_256(password):
    encoded = password.encode()
    result = hashlib.sha256(encoded)
    return result.hexdigest()

def find_user(password):
    database = r'/home/morkovka/PycharmProjects/Mnworkie/flaskie_app/updated_mnatabase.db'
    conn = ConnectionDB.create_conn(database)
    sql = "SELECT id FROM users WHERE password=?"


    cur = conn.cursor()
    cur.execute(sql, (password,))

    row = cur.fetchone()
    return row

print(find_user('slut'))


print(hashing_256('morkovka.13'))
print(hashing_256('lovefamily#14'))
print(hashing_256('somepword5'))
