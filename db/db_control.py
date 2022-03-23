import sqlite3
from sqlite3 import Error, Row


class ConnectionDB:


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
    def create_table(cls, conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    @classmethod
    def add_user(cls, conn, user):
        sql = """INSERT INTO users (username, password)
             VALUES(?,?)"""
        cur = conn.cursor()

        cur.execute(sql, user)
        with conn:
            conn.commit()


    @classmethod
    def show_todos(cls, conn, user_id):
        all_todos = []
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = """SELECT id, name, done FROM todos
                    WHERE user_id=?"""
        cur.execute(sql, (user_id,))

        rows = cur.fetchall()
        for row in rows:
            all_todos.append(dict(zip(row.keys(), row)))
        return all_todos

    @classmethod
    def create_todo(cls, conn, todo):
        sql = """INSERT INTO todos (name, description, user_id, done)
         VALUES(?,?,?,?)"""
        cur = conn.cursor()

        cur.execute(sql, todo)
        with conn:
            conn.commit()






    @classmethod
    def delete_todo(cls, conn, id):
        sql = "DELETE FROM todos WHERE id=?"
        cur = conn.cursor()
        cur.execute(sql, (id,))
        conn.commit()

    @classmethod
    def upsert_todo(cls, conn, todo_parameters):
        sql = """INSERT INTO todos (id, name, description, user_id, done) VALUES(?,?,?,?,?)
                    ON CONFLICT(id) DO UPDATE SET
                    name = excluded.name,
                    description = excluded.description,
                    done = excluded.done;
               """
        cur = conn.cursor()
        cur.execute(sql, todo_parameters)
        conn.commit()


    @classmethod
    def show_single_todo(cls, conn, id):
        sql = "SELECT name, description, done FROM todos WHERE id=? "
        cur = conn.cursor()
        cur.execute(sql, (id,))
        row = cur.fetchone()
        return row

    @classmethod
    def check_user(cls, username, password):
        database = r'/home/morkovka/PycharmProjects/Mnworkie/flaskie_app/updated_mnatabase.db'
        conn = ConnectionDB.create_conn(database)
        sql = "SELECT id FROM users WHERE username=? AND password=?"


        cur = conn.cursor()
        cur.execute(sql,
                   (username, password)
                    )
        row = cur.fetchone()
        return row







def main():
    database = r'/home/morkovka/PycharmProjects/Mnworkie/flaskie_app/updated_mnatabase.db'
    conn = ConnectionDB.create_conn(database)
    sql_create_todos = """CREATE TABLE IF NOT EXISTS todos (
                                                         id integer PRIMARY KEY,
                                                         name text NOT NULL,
                                                         description text,
                                                         user_id integer NOT NULL,
                                                         done integer NOT NULL,
                                                         FOREIGN KEY(user_id) REFERENCES users(id)
                                                         
                                                         );"""
    sql_create_users = """CREATE TABLE IF NOT EXISTS users (
                                                        id integer PRIMARY KEY,
                                                        username text NOT NULL,
                                                        password text NOT NULL
                                                        );"""


    # ConnectionDB.create_table(conn, sql_create_todos)
    todo1 = ("cook some korean chicken", "deep fry until done!", 1, 0)
    todo2 = ("complete the javascript course", "go through the exercises", 1, 0)
    todo3 = ("some junk", "alala", 0, 1)
    todo4 = ("get rid of heartburn again please", "idfk know how", 0, 2)
    user1 = ('mniammy', 'iloveyou256')
    with conn:
        print(ConnectionDB.add_user(conn, user1))



if __name__ == "__main__":
    main()




