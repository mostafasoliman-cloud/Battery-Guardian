from core.battery import Battery
from core.notifier import Notifier

from config import (
    CRITICAL_BATTERY,
    FULL_BATTERY,
    LOW_BATTERY,
)


class BatteryMonitor:

    def __init__(self, database):
        self.database = database

        self.low_notified = False
        self.critical_notified = False
        self.full_notified = False

        self.previous_plugged = None

    def check(self):
        info = Battery.get_info()

        if info is None:
            return None

        percentage = info["percent"]
        plugged = info["plugged"]

        self.database.add_log(
            percentage,
            plugged,
            info["seconds_left"]
        )

        if self.previous_plugged is False and plugged is True:
            Notifier.send(
                "Charger Connected",
                f"Battery: {percentage}%"
            )

        elif self.previous_plugged is True and plugged is False:
            Notifier.send(
                "Charger Disconnected",
                f"Battery: {percentage}%"
            )

        # Critical battery takes priority over the low-battery alert.
        if percentage <= CRITICAL_BATTERY and not plugged:
            if not self.critical_notified:
                Notifier.send(
                    "Critical Battery",
                    f"Battery is only {percentage}%"
                )
                self.critical_notified = True

            self.low_notified = True

        elif percentage <= LOW_BATTERY and not plugged:
            self.critical_notified = False

            if not self.low_notified:
                Notifier.send(
                    "Low Battery",
                    f"Battery is {percentage}%"
                )
                self.low_notified = True

        else:
            self.low_notified = False
            self.critical_notified = False

        if percentage >= FULL_BATTERY and plugged:
            if not self.full_notified:
                Notifier.send(
                    "Battery Full",
                    "Battery reached 100%."
                )
                self.full_notified = True
        else:
            self.full_notified = False

        self.previous_plugged = plugged

        return info
