from winotify import Notification

from config import APP_NAME


class Notifier:

    @staticmethod
    def send(title, message):
        notification = Notification(
            app_id=APP_NAME,
            title=title,
            msg=message
        )
        notification.show()
