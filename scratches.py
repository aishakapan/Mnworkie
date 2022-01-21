import sqlite3
from sqlite3 import Error
from db_control import ConnectionDB

database = r'C:\Users\aisha\PycharmProjects\Mnworkie\mnatabase.db'
conn = ConnectionDB.create_conn(database)


def fetch_rows():
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('select * from todos')
    rows = cur.fetchone()
    return rows.keys()

print(fetch_rows())
conn = ConnectionDB.create_conn('mnatabase.db')
data = list(ConnectionDB.show_todos(conn))
print(data)
rows = fetch_rows()
combined = list(zip(rows, *data))
print(combined)

sql_create_users = """CREATE TABLE IF NOT EXISTS users(
                                                    id integer PRIMARY KEY,
                                                    username text NOT NULL,
                                                    password NOT NULL
                                                    );"""
sql_create_todos = """CREATE TABLE IF NOT EXISTS todos(
                                                    id integer PRIMARY KEY,
                                                    name text NOT NULL,
                                                    description text,
                                                    done integer NOT NULL,
                                                    user_id integer NOT NULL,
                                                    FOREIGN KEY(user_id) REFERENCES users(id)
                                                    );"""
if conn is not None:
    ConnectionDB.create_table(conn, sql_create_users)
    ConnectionDB.create_table(conn, sql_create_todos)