from database.db import Database
from core.monitor import BatteryMonitor
from gui.dashboard import Dashboard


def main():

    database = Database()

    monitor = BatteryMonitor(
        database
    )

    app = Dashboard(
        monitor
    )

    app.mainloop()


if __name__ == "__main__":
    main()