import sqlite3

class Database(object):
    dbLocation = "botdatabase.db"

    def __init__(self):
        self.connection = sqlite3.connect(Database.dbLocation)
        self.sql = self.connection.cursor()

    # Used to send a single query
    def execute(self, query):
        return self.sql.execute(query)

    # Can send query with an array to insert multiple rows at once
    def executeMany(self, query, data):
        self.sql.executemany(query, data)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.sql.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()