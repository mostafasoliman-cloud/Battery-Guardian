import sqlite3
from datetime import datetime
from pathlib import Path


class Database:

    def __init__(self, db_name="data/battery.db"):
        self.db_path = Path(db_name)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(
            self.db_path,
            check_same_thread=False
        )

        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS battery_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            percentage INTEGER NOT NULL,
            plugged INTEGER NOT NULL,
            seconds_left INTEGER
        )
        """

        self.connection.execute(query)
        self.connection.commit()

    def add_log(self, percentage, plugged, seconds_left):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

        cursor = self.connection.execute(query, (limit,))
        return cursor.fetchall()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
