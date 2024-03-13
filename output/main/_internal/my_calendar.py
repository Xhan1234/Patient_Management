import calendar
import tkinter as tk
from datetime import datetime

class PersonalizedCalendar(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Personalized Calendar")

        # Get the current date
        self.current_year = tk.IntVar()
        self.current_month = tk.IntVar()
        self.current_day = tk.IntVar()

        now = datetime.now()  # Get the current date and time
        self.current_year.set(now.year)
        self.current_month.set(now.month)
        self.current_day.set(now.day)

        # Create labels to display the current date, month, and selected date
        self.date_label = tk.Label(self, text=self.get_current_date(), font=("Arial", 16))
        self.date_label.pack(pady=10)

        self.selected_date_label = tk.Label(self, text=self.current_day.get(), font=("Arial", 20, "bold"))
        self.selected_date_label.pack(pady=5)

        # Create a frame to hold the calendar
        self.calendar_frame = tk.Frame(self)
        self.calendar_frame.pack()

        # Create buttons to navigate the calendar
        self.prev_button = tk.Button(self, text="<< Prev", command=self.prev_month)
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.next_button = tk.Button(self, text="Next >>", command=self.next_month)
        self.next_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Create a button to save the selected date
        self.save_button = tk.Button(self, text="Save Date", command=self.save_date)
        self.save_button.pack(pady=10)

        # Display the calendar
        self.create_calendar()

    def get_current_date(self):
        month_name = calendar.month_name[self.current_month.get()]
        return f"{month_name} {self.current_year.get()}"

    def create_calendar(self):
        # Clear any existing calendar widgets
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Get the calendar for the current month and year
        cal = calendar.monthcalendar(self.current_year.get(), self.current_month.get())

        # Create labels to display the days of the week
        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days_of_week):
            label = tk.Label(self.calendar_frame, text=day)
            label.grid(row=0, column=i, padx=5, pady=5)

        # Create labels to display the calendar days
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day != 0:
                    label = tk.Label(self.calendar_frame, text=day, cursor="hand2")
                    label.grid(row=week_num + 1, column=day_num, padx=5, pady=5)
                    label.bind("<Button-1>", lambda event, day=day: self.select_date(day))

    def select_date(self, selected_day):
        self.current_day.set(selected_day)
        self.date_label.config(text=self.get_current_date())
        self.selected_date_label.config(text=self.current_day.get(), font=("Arial", 20, "bold"))

    def save_date(self):
        selected_date = "{}-{}-{}".format(self.current_year.get(), self.current_month.get(), self.current_day.get())
        print("Selected date:", selected_date)

    def prev_month(self):
        # Decrement the current month
        self.current_month.set(self.current_month.get() - 1)
        if self.current_month.get() == 0:
            self.current_month.set(12)
            self.current_year.set(self.current_year.get() - 1)

        # Update the calendar
        self.create_calendar()
        self.date_label.config(text=self.get_current_date())

    def next_month(self):
        # Increment the current month
        self.current_month.set(self.current_month.get() + 1)
        if self.current_month.get() == 13:
            self.current_month.set(1)
            self.current_year.set(self.current_year.get() + 1)

        # Update the calendar
        self.create_calendar()
        self.date_label.config(text=self.get_current_date())

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Personalized Calendar")

    # Create the personalized calendar
    personalized_calendar = PersonalizedCalendar(root)
    personalized_calendar.geometry("400x400+100+100")  # Set size and position

    root.mainloop()
