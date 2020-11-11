import sqlite3

db_name = 'data.db'
SESSIONS_TABLE = 'sessions'


class DB_bot:
    def __init__(self):
        self.conn = self.get_connect()
        self.c = self.conn.cursor()
        self.create_table()

    def get_connect(self):
        conn = sqlite3.connect(db_name)
        return conn

    def create_table(self):
        self.conn.execute(f"""CREATE TABLE if not exists {SESSIONS_TABLE}
                                                           (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            title text,
                                                            duration integer,
                                                            executable_path text,
                                                            start_date integer)
                                                                   """)

    def getter(self, id, column):
        if id:
            return self.c.execute(f"SELECT {column} FROM {SESSIONS_TABLE} WHERE id=?", (id,)).fetchall()[0][0]
        else:
            return self.c.execute(f"SELECT {column} FROM {SESSIONS_TABLE}").fetchall()[0]

    def setter(self, id, column, value):
        if id:
            res = self.c.execute(f"""
                                UPDATE {SESSIONS_TABLE}
                                SET {column} = ?
                                WHERE id = {id}""", (value,))
            self.conn.commit()
            return res
        else:
            return False

    # def get_name(self, id):
    #     return self.getter(id, "name")
    #
    # def get_time_use(self, id):
    #     return self.getter(id, 'time_use')
    #
    # def get_date(self, id):
    #     return self.getter(id, "date")
    #
    # def set_name(self, id, value):
    #     return self.setter(id, "name", value)
    #
    # def set_time_use(self, id, value):
    #     return self.setter(id, "time_use", value)
    #
    def set_duration(self, id, value):
        return self.setter(id, "duration", value)

    # another methods

    def create_new_session(self, *args):
        self.c.executemany(f"INSERT INTO {SESSIONS_TABLE} VALUES({','.join(['?' for _ in args])})", (args,))
        self.conn.commit()

    def set_duration_last_session(self, duration):
        session_id = self.c.execute(f'SELECT id FROM {SESSIONS_TABLE}'
                                    f' WHERE ID = (SELECT MAX(ID) FROM {SESSIONS_TABLE});').fetchall()[0][0]
        self.set_duration(session_id, duration)

    def delete_all_sessions(self):
        self.c.execute(f'DELETE FROM {SESSIONS_TABLE}')
        self.conn.commit()

    def get_sessions_by_date(self, start_date):
        return self.c.execute(
            f'SELECT * FROM {SESSIONS_TABLE} WHERE start_date>={start_date} ORDER BY start_date').fetchall()

    def delete_old(self, start_date):
        self.c.execute(f'DELETE FROM {SESSIONS_TABLE} WHERE start_date < {start_date}')
