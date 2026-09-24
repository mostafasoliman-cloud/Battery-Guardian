import psutil


class Battery:

    @staticmethod
    def get_info():
        battery = psutil.sensors_battery()

        if battery is None:
            return None

        return {
            "percent": battery.percent,
            "plugged": battery.power_plugged,
            "seconds_left": battery.secsleft
        }

    @staticmethod
    def get_time_left(seconds):
        if seconds is None or seconds <= 0:
            return "Unknown"

        hours, remainder = divmod(seconds, 3600)
        minutes = remainder // 60

        return f"{hours}h {minutes}m"
