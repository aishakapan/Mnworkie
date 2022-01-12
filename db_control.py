import sqlite3
from sqlite3 import Error


class ConnectionDB:
    @classmethod
    def show_todos(cls, conn):
        cur = conn.cursor()
        cur.execute("SELECT *FROM todos")
        todos = cur.fetchall()
        return todos

    @classmethod
    def create_conn(cls, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    @classmethod
    def create_todo(cls,conn, todo):
        sql = """ INSERT INTO todos (name, description, user_id, done)
         VALUES(?,?,?,?) """
        cur = conn.cursor()
        cur.execute(sql, todo)
        conn.commit()



    @classmethod
    def update_todo(cls):
        pass

    @classmethod
    def delete_todo(cls):
        pass

    @classmethod
    def show_single_todo(cls):
        pass



def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r'C:\Users\aisha\PycharmProjects\Mnworkie\mnatabase.db'

    conn = ConnectionDB.create_conn(database)
    todo1 = ("make a dinner", "fry some zucchinis", 1, 1)
    with conn:
        ConnectionDB.create_todo(conn, todo1)


if __name__ == "__main__":
    main()
