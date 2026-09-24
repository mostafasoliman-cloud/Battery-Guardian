import sqlite3
from datetime import datetime


class Database:

    def __init__(self, db_name="data/battery.db"):

        self.connection = sqlite3.connect(
            db_name,
            check_same_thread=False
        )

        self.create_table()

    def create_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS battery_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            percentage INTEGER,

            plugged INTEGER,

            seconds_left INTEGER

        )
        """

        self.connection.execute(query)
        self.connection.commit()

    def add_log(self, percentage, plugged, seconds_left):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        query = """
        INSERT INTO battery_logs
        (timestamp, percentage, plugged, seconds_left)

        VALUES (?, ?, ?, ?)
        """

        self.connection.execute(
            query,
            (
                timestamp,
                percentage,
                int(plugged),
                seconds_left
            )
        )

        self.connection.commit()

    def get_recent_logs(self, limit=20):

        query = """
        SELECT timestamp, percentage, plugged
        FROM battery_logs
        ORDER BY id DESC
        LIMIT ?
        """

        cursor = self.connection.execute(
            query,
            (limit,)
        )

        return cursor.fetchall()