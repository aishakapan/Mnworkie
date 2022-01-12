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

