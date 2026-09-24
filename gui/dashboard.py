import customtkinter as ctk

from core.battery import Battery


class Dashboard(ctk.CTk):

    def __init__(self, monitor):

        super().__init__()

        self.monitor = monitor

        self.title("Battery Guardian")
        self.geometry("500x400")

        ctk.set_appearance_mode("dark")

        # -------------------------
        # Title
        # -------------------------

        self.title_label = ctk.CTkLabel(
            self,
            text="🔋 Battery Guardian",
            font=("Arial", 28, "bold")
        )

        self.title_label.pack(pady=25)

        # -------------------------
        # Battery %
        # -------------------------

        self.battery_label = ctk.CTkLabel(
            self,
            text="--%",
            font=("Arial", 50, "bold")
        )

        self.battery_label.pack(pady=10)

        # -------------------------
        # Progress
        # -------------------------

        self.progress = ctk.CTkProgressBar(
            self,
            width=350
        )

        self.progress.pack(pady=15)

        self.progress.set(0)

        # -------------------------
        # Status
        # -------------------------

        self.status_label = ctk.CTkLabel(
            self,
            text="Status: --",
            font=("Arial", 18)
        )

        self.status_label.pack(pady=10)

        # -------------------------
        # Time
        # -------------------------

        self.time_label = ctk.CTkLabel(
            self,
            text="Time Left: --",
            font=("Arial", 18)
        )

        self.time_label.pack(pady=10)

        self.update_dashboard()

    def update_dashboard(self):

        info = self.monitor.check()

        if info:

            percentage = info["percent"]
            plugged = info["plugged"]
            seconds = info["seconds_left"]

            self.battery_label.configure(
                text=f"{percentage}%"
            )

            self.progress.set(
                percentage / 100
            )

            if plugged:

                self.status_label.configure(
                    text="Status: Charging 🔌"
                )

            else:

                self.status_label.configure(
                    text="Status: Discharging ⚡"
                )

            self.time_label.configure(
                text=f"Time Left: {Battery.get_time_left(seconds)}"
            )

        self.after(
            60000,
            self.update_dashboard
        )