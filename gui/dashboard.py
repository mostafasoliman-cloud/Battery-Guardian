import customtkinter as ctk

from config import CHECK_INTERVAL
from core.battery import Battery


class Dashboard(ctk.CTk):

    def __init__(self, monitor):
        super().__init__()

        self.monitor = monitor
        self.after_id = None

        self.title("Battery Guardian")
        self.geometry("500x400")
        self.protocol("WM_DELETE_WINDOW", self.close)

        ctk.set_appearance_mode("dark")

        self.title_label = ctk.CTkLabel(
            self,
            text="Battery Guardian",
            font=("Arial", 28, "bold")
        )
        self.title_label.pack(pady=25)

        self.battery_label = ctk.CTkLabel(
            self,
            text="--%",
            font=("Arial", 50, "bold")
        )
        self.battery_label.pack(pady=10)

        self.progress = ctk.CTkProgressBar(
            self,
            width=350
        )
        self.progress.pack(pady=15)
        self.progress.set(0)

        self.status_label = ctk.CTkLabel(
            self,
            text="Status: --",
            font=("Arial", 18)
        )
        self.status_label.pack(pady=10)

        self.time_label = ctk.CTkLabel(
            self,
            text="Time Left: --",
            font=("Arial", 18)
        )
        self.time_label.pack(pady=10)

        self.update_dashboard()

    def update_dashboard(self):
        info = self.monitor.check()

        if info is None:
            self.status_label.configure(
                text="Status: Battery not available"
            )
        else:
            percentage = info["percent"]
            plugged = info["plugged"]
            seconds = info["seconds_left"]

            self.battery_label.configure(
                text=f"{percentage}%"
            )

            self.progress.set(percentage / 100)

            status = "Charging" if plugged else "Discharging"
            self.status_label.configure(
                text=f"Status: {status}"
            )

            self.time_label.configure(
                text=f"Time Left: {Battery.get_time_left(seconds)}"
            )

        self.after_id = self.after(
            CHECK_INTERVAL * 1000,
            self.update_dashboard
        )

    def close(self):
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.monitor.database.close()
        self.destroy()
