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

        if seconds <= 0:
            return "Unknown"

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        return f"{hours}h {minutes}m"