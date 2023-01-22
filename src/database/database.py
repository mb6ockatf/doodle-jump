"""
Class to work with database
"""
from os import path, getcwd
from sqlite3 import connect


class DatabaseConnection:
    """
    handle DB connection and queries execution
    """
    def __init__(self):
        db_path = path.realpath(path.join(getcwd(), "records.db"))
        if not path.isfile(db_path):
            open(db_path, "w", encoding="utf-8").close()
        self.connection = connect(db_path)
        query = """
        CREATE TABLE IF NOT EXISTS main (
            nickname TEXT UNIQUE NOT NULL,
            record INTEGER UNSIGNED DEFAULT 0);
        """
        self._execute(query, None)

    def close(self):
        """
        Close database connection
        """
        self.connection.close()

    def _execute(self, query: str, data) -> list:
        """
        Execute SQL query with values
        """
        cursor = self.connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return result

    def insert(self, nickname: str, value: int):
        """
        insert new record into database
        """
        data = {"nickname": nickname, "value": value}
        query = """
        SELECT record FROM main
        WHERE nickname = :nickname;
        """
        result = self._execute(query, data)
        query = """
        INSERT OR REPLACE INTO main
        (nickname, record)
        VALUES (:nickname, :value);
        """
        answer = None
        write = False
        if result == []:
            write = True
        elif result[0][0] < data["value"]:
            write = True
        if write:
            answer = self._execute(query, data)
        return answer

    def select(self, nickname: str):
        """
        insert new record into database
        """
        data = {"nickname": nickname}
        query = """
        SELECT record
        FROM main
        WHERE nickname = :nickname;
        """
        result = self._execute(query, data)
        return result
