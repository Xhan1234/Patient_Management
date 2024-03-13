# frontend
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox, ttk

import backend as be
from my_calendar import PersonalizedCalendar


class LoginScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Doctor Login')
        self.configure(bg='#f0f0f0')  # Set background color

        # Create tables
        be.create_tables()

        # Define font style
        font_style = ("Arial", 12)

        self.username_label = tk.Label(
            self,
            text="Username:",
            font=font_style,
            bg='#f0f0f0',  # Background color
            fg='#333333'  # Text color
        )
        self.username_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )
        self.username_entry = tk.Entry(
            self,
            font=font_style
        )
        self.username_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=5,
            sticky="ew"
        )

        self.password_label = tk.Label(
            self,
            text="Password:",
            font=font_style,
            bg='#f0f0f0',  # Background color
            fg='#333333'  # Text color
        )
        self.password_label.grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )
        self.password_entry = tk.Entry(
            self,
            show="*",  # Hide password
            font=font_style
        )
        self.password_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=5,
            sticky="ew"
        )

        self.login_button = tk.Button(
            self,
            text="Login",
            font=font_style,
            bg='#4caf50',  # Background color
            fg='white',  # Text color
            command=self.login
        )
        self.login_button.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.register_button = tk.Button(
            self,
            text="Register",
            font=font_style,
            bg='#2196f3',  # Background color
            fg='white',  # Text color
            command=self.register_doctor
        )
        self.register_button.grid(
            row=3,
            column=0,  # This column position overlaps with the previous button
            columnspan=2,
            padx=10,
            pady=10,
            sticky="ew"
        )

        # Calculate the required width and height for the window based on widget sizes and padding
        window_width = max(self.winfo_reqwidth(), 300)
        window_height = max(self.winfo_reqheight(), 250)

        # Adjust the window geometry to fit the content
        self.geometry(f"{window_width}x{window_height}")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the user is an admin
        if username == "admin" and password == "17021997":
            role = "admin"
        else:
            role = "doctor"

        doctor_info = be.login(username, password, None)  # Pass the role parameter to the login function

        if doctor_info:
            doctor_id, _ = doctor_info  # Extract doctor_id from the returned tuple
            doctor_name = be.get_doctor_name(doctor_id)  # Ensure doctor_id is an integer

            if doctor_name:
                self.destroy()  # Close login window
                app = App(doctor_id, doctor_name, role)  # Pass the role parameter here
                app.mainloop()
            else:
                messagebox.showerror("Error", "Failed to retrieve doctor's name.")
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register_doctor(self):
        register_window = RegisterDoctorWindow(self)
        register_window.mainloop()


class RegisterDoctorWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Register Doctor')
        self.geometry('400x150')  # Adjusted height for simplicity
        self.configure(bg='#f0f0f0')  # Set background color
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        # Define font style
        font_style = ("Arial", 12)

        self.username_label = tk.Label(
            self,
            text="Username:",
            font=font_style,
            bg='#f0f0f0',  # Background color
            fg='#333333'  # Text color
        )
        self.username_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )
        self.username_entry = tk.Entry(
            self,
            font=font_style
        )
        self.username_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=5,
            sticky="ew"
        )

        self.password_label = tk.Label(
            self,
            text="Password:",
            font=font_style,
            bg='#f0f0f0',  # Background color
            fg='#333333'  # Text color
        )
        self.password_label.grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )
        self.password_entry = tk.Entry(
            self,
            show="*",  # Hide password
            font=font_style
        )
        self.password_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=5,
            sticky="ew"
        )

        # Removed role entry widget
        # Automatically set role to 'doctor'
        role = 'doctor'

        self.register_button = tk.Button(
            self,
            text="Register",
            font=font_style,
            bg='#4caf50',  # Background color
            fg='white',  # Text color
            command=self.register_doctor
        )
        self.register_button.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="ew"
        )

    def register_doctor(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = 'doctor'  # Set role to 'doctor'
        if be.register_doctor(username, password, role):
            self.destroy()  # Close the current window after successful registration


class App(tk.Tk):
    def __init__(self, doctor_id, doctor_name, role):
        super().__init__()
        self.selected_start_date = None  # Variable to store the selected start date
        self.selected_end_date = None  # Variable to store the selected end date
        # Determine screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.role = role  # Store the role attribute
        self.crud_window_open = False  # Initialize the flag

        # Calculate the window size
        window_width = int(screen_width * 0.99)
        window_height = int(screen_height * 0.88)

        # Set the window size and position
        self.geometry(
            f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")

        self.title(f"Patient Management App")
        self.configure(bg='#f0f0f0')  # Set background color

        # Initialize patient_ids list
        self.patient_ids = []
        self.doctor_id = doctor_id
        self.doctor_name = doctor_name
        self.role = role  # Store the role
        self.selected_start_date = None  # Variable to store the selected start date
        self.selected_end_date = None  # Variable to store the selected end date

        # Frame to contain entry fields and button for adding patient
        self.entry_frame = tk.Frame(self, bg='#f0f0f0')
        self.entry_frame.pack(fill=tk.BOTH)

        if role != 'admin':
            # Entry field for Name
            self.name_label = tk.Label(
                self.entry_frame,
                text="Name:",
                font=("Arial", 14, "bold"),
                bg='#f0f0f0',  # Background color
                fg='#333333'  # Text color
            )
            self.name_label.grid(row=0, column=0, padx=10, pady=10)
            self.name_entry = tk.Entry(
                self.entry_frame,
                font=("Arial", 12)
            )
            self.name_entry.grid(row=0, column=1, padx=10, pady=10)

            # Entry field for Surname
            self.surname_label = tk.Label(
                self.entry_frame,
                text="Surname:",
                font=("Arial", 14, "bold"),
                bg='#f0f0f0',  # Background color
                fg='#333333'  # Text color
            )
            self.surname_label.grid(row=0, column=2, padx=10, pady=10)
            self.surname_entry = tk.Entry(
                self.entry_frame,
                font=("Arial", 12)
            )
            self.surname_entry.grid(row=0, column=3, padx=10, pady=10)

            # Entry field for Diagnosis
            self.diagnosis_label = tk.Label(
                self.entry_frame,
                text="Diagnosis:",
                font=("Arial", 14, "bold"),
                bg='#f0f0f0',  # Background color
                fg='#333333'  # Text color
            )
            self.diagnosis_label.grid(row=0, column=4, padx=10, pady=10)
            self.diagnosis_entry = tk.Text(
                self.entry_frame,
                font=("Arial", 12),
                height=5,
                width=50
            )
            self.diagnosis_entry.grid(row=0, column=5, padx=10, pady=10)

            # Add Patient button
            self.add_patient_button = tk.Button(
                self.entry_frame,
                text="Add Patient",
                font=("Arial", 14, "bold"),
                bg='#4caf50',  # Background color
                fg='white',  # Text color
                command=self.add_patient,
                width=12  # Set a fixed width
            )
            self.add_patient_button.grid(row=0, column=6, padx=10, pady=10)

        # Frame to contain entry fields and button for filtering
        self.filter_frame = tk.Frame(self, bg='#f0f0f0')
        self.filter_frame.pack(fill=tk.BOTH)

        # Entry field for Name filter
        self.filter_name_label = tk.Label(
            self.filter_frame,
            text="Name:",
            font=("Arial", 14, "bold"),
            bg='#f0f0f0',  # Background color
            fg='#333333'  # Text color
        )
        self.filter_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.filter_name_entry = tk.Entry(
            self.filter_frame,
            font=("Arial", 12)
        )
        self.filter_name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Entry field for Surname filter
        self.filter_surname_label = tk.Label(
            self.filter_frame,
            text="Surname:",
            font=("Arial", 14, "bold"),
            bg='#f0f0f0',  # Background color
            fg='#333333'  # Text color
        )
        self.filter_surname_label.grid(row=0, column=2, padx=10, pady=10)
        self.filter_surname_entry = tk.Entry(
            self.filter_frame,
            font=("Arial", 12)
        )
        self.filter_surname_entry.grid(row=0, column=3, padx=10, pady=10)

        # Button to show calendar for Start Date filter
        self.show_start_date_calendar_button = tk.Button(
            self.filter_frame,
            text="Select Start Date",
            font=("Arial", 14, "bold"),
            bg='#2196f3',  # Background color
            fg='white',  # Text color
            command=self.show_start_date_calendar
        )
        self.show_start_date_calendar_button.grid(row=0, column=4, padx=10, pady=10)

        # Label to show selected Start Date
        self.selected_start_date_label = tk.Label(
            self.filter_frame,
            text="",
            font=("Arial", 12),
            bg='#f0f0f0',  # Background color
            fg='#333333'  # Text color
        )
        self.selected_start_date_label.grid(row=0, column=5, padx=10, pady=10)

        # Button to show calendar for End Date filter
        self.show_end_date_calendar_button = tk.Button(
            self.filter_frame,
            text="Select End Date",
            font=("Arial", 14, "bold"),
            bg='#2196f3',  # Background color
            fg='white',  # Text color
            command=self.show_end_date_calendar
        )
        self.show_end_date_calendar_button.grid(row=0, column=6, padx=10, pady=10)

        # Label to show selected End Date
        self.selected_end_date_label = tk.Label(
            self.filter_frame,
            text="",
            font=("Arial", 12),
            bg='#f0f0f0',  # Background color
            fg='#333333'  # Text color
        )
        self.selected_end_date_label.grid(row=0, column=7, padx=10, pady=10)

        # Filter button
        self.filter_button = tk.Button(
            self.filter_frame,
            text="Filter",
            font=("Arial", 14, "bold"),
            bg='#4caf50',  # Background color
            fg='white',  # Text color
            command=self.filter_patients,
            width=12  # Set a fixed width
        )
        self.filter_button.grid(row=0, column=8, padx=10, pady=10)

        # Button to clear filtering
        self.clear_filter_button = tk.Button(
            self.filter_frame,
            text="Clear Filter",
            font=("Arial", 14, "bold"),
            bg='#f44336',  # Background color
            fg='white',  # Text color
            command=self.clear_filter_fields,
            width=12  # Set a fixed width
        )
        self.clear_filter_button.grid(row=0, column=9, padx=10, pady=10)

        # Create Treeview widget
        self.tree = ttk.Treeview(self, columns=("Name", "Surname", "Diagnosis", "Date"), show="headings",
                                 style="Custom.Treeview")
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.tree.pack(fill="both", expand=True)

        # Define custom style for Treeview
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview.Heading", font=("Arial", 14, "bold"))  # Style for column headings
        self.style.configure("Custom.Treeview", font=("Arial", 14), padding=10)  # Adjust padding to increase space
        self.style.map("Custom.Treeview", foreground=[('selected', '#ffffff')], background=[('selected', '#0078d7')])
        self.style.map("Custom.Treeview", rowheight=[('selected', 100)])  # Increase row height

        # Adjust column headings

        self.tree.heading("Name", text="Name", anchor=tk.CENTER)
        self.tree.heading("Surname", text="Surname", anchor=tk.CENTER)
        self.tree.heading("Diagnosis", text="Diagnosis", anchor=tk.CENTER)
        self.tree.heading("Date", text="Date", anchor=tk.CENTER)

        # Adjust column widths

        self.tree.column("Name", width=100, anchor=tk.CENTER)
        self.tree.column("Surname", width=100, anchor=tk.CENTER)
        self.tree.column("Diagnosis", width=200, anchor=tk.CENTER)
        self.tree.column("Date", width=100, anchor=tk.CENTER)

        # Adjust row spacing
        self.tree.tag_configure("spaced")  # Set spacing between rows

        self.patient_count_label = tk.Label(
            self,
            text="Total Patients: 0",
            font=("Arial", 12),
            bg='#f0f0f0',  # Background color
            fg='#333333'  # Text color
        )
        self.patient_count_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Pagination variables
        self.page_size = 10  # Number of patients per page
        self.current_page = 1  # Current page number

        # Navigation buttons
        self.prev_button = tk.Button(self, text="Prev", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.next_button = tk.Button(self, text="Next", command=self.next_page)
        self.next_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Logout button
        self.logout_button = tk.Button(
            self,
            text="Logout",
            font=("Arial", 14, "bold"),
            bg='#f44336',  # Background color
            fg='white',  # Text color
            command=self.logout
        )
        self.logout_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Doctor name label
        self.doctor_name_label = tk.Label(
            self,
            text=f"Logged in as Dr. {doctor_name}",
            font=("Arial", 12),
            bg='#f0f0f0',  # Background color
            fg='#333333'  # Text color
        )
        self.doctor_name_label.pack(side=tk.RIGHT, padx=10, pady=10)

        if role == 'admin':
            # Button to open a window to delete doctors
            self.delete_doctor_button = tk.Button(
                self,
                text="Delete Doctor",
                font=("Arial", 14, "bold"),
                bg='#f3212d',  # Background color
                fg='white',  # Text color
                command=self.open_delete_doctor_window
            )
            self.delete_doctor_button.pack(side=tk.LEFT, padx=10, pady=10)

        if role == 'admin':
            # Add UI elements for updating doctor password
            self.update_password_button = tk.Button(
                self,
                text="Update Doctor Password",
                font=("Arial", 14, "bold"),
                bg='#0a6ebd',
                fg='white',
                command=self.open_update_password_window
            )
            self.update_password_button.pack(pady=10)

        # Update patient count label
        self.populate_patients_list()  # Populate patient list
        self.update_patient_count_label()

    def add_spacing_rows(self, data_count):
        # Add empty rows between data rows for spacing
        for i in range(1, data_count):
            # Insert a spacing row after every data row
            self.tree.insert("", f"end", values=("", "", "", ""), tags=("spaced",))

    def update_patients_list(self):
        # Calculate start and end indices for the current page
        start_index = (self.current_page - 1) * self.page_size
        end_index = start_index + self.page_size

        # Fetch patients from the database
        patients = be.get_patients(self.doctor_id)

        # Filter patients for the current page
        patients_on_current_page = patients[start_index:end_index]

        # Clear previous entries
        self.tree.delete(*self.tree.get_children())

        # Populate the Treeview with patient data for the current page
        for i, patient in enumerate(patients_on_current_page):
            # Ensure the order of values matches the order of columns in the Treeview
            self.tree.insert("", "end", values=(patient[2], patient[3], patient[4], patient[5]))

            # Add empty rows between data rows for spacing
            if i < len(patients_on_current_page) - 0.5:
                self.tree.insert("", "end", values=("", "", "", ""), tags=("spaced",))

        # Update patient count label to show the current page and total pages
        total_patients = len(patients)
        total_pages = (total_patients + self.page_size - 1) // self.page_size
        self.patient_count_label.config(
            text=f"Page {self.current_page}/{total_pages}, Total Patients: {total_patients}")

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_patients_list()

    def next_page(self):
        total_patients = len(be.get_patients(self.doctor_id))
        total_pages = (total_patients + self.page_size - 1) // self.page_size
        if self.current_page < total_pages:
            self.current_page += 1
            self.populate_patients_list()

    # Function to handle updating doctor password
    def open_update_password_window(self):
        # Create a new window for updating password
        update_password_window = tk.Toplevel(self)
        update_password_window.title("Update Password")

        # Entry field for username
        username_label = tk.Label(update_password_window, text="Username:", font=("Arial", 12), bg='#f0f0f0',
                                  fg='#333333')
        username_label.grid(row=0, column=0, padx=10, pady=10)
        username_entry = tk.Entry(update_password_window, font=("Arial", 12))
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Entry field for new password
        password_label = tk.Label(update_password_window, text="New Password:", font=("Arial", 12), bg='#f0f0f0',
                                  fg='#333333')
        password_label.grid(row=1, column=0, padx=10, pady=10)
        password_entry = tk.Entry(update_password_window, font=("Arial", 12))
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Button to update password
        update_button = tk.Button(
            update_password_window,
            text="Update",
            font=("Arial", 14, "bold"),
            bg='#4caf50',  # Background color
            fg='white',  # Text color
            command=lambda: self.update_doctor_password(username_entry, password_entry, update_password_window)
        )
        update_button.grid(row=2, columnspan=2, padx=10, pady=10)

    def open_delete_doctor_window(self):
        # Create a new window to display registered doctors and allow deletion
        delete_doctor_window = tk.Toplevel(self)
        delete_doctor_window.title("Delete Doctor")

        # Label to display instructions
        instructions_label = tk.Label(
            delete_doctor_window,
            text="Select a doctor to delete:",
            font=("Arial", 14),
            bg='#f0f0f0',  # Background color
            fg='#333333'  # Text color
        )
        instructions_label.pack(pady=10)

        # Listbox to display registered doctors
        doctor_listbox = tk.Listbox(
            delete_doctor_window,
            font=("Arial", 12),
            selectmode=tk.SINGLE
        )
        doctor_listbox.pack(pady=10)

        # Fetch registered doctors from the backend
        registered_doctors = be.fetch_registered_doctors()

        # Populate the listbox with registered doctors
        for doctor in registered_doctors:
            doctor_listbox.insert(tk.END, doctor)

        # Button to delete the selected doctor
        delete_button = tk.Button(
            delete_doctor_window,
            text="Delete",
            font=("Arial", 14, "bold"),
            bg='#f44336',  # Background color
            fg='white',  # Text color
            command=lambda: self.delete_selected_doctor(doctor_listbox, delete_doctor_window)
        )
        delete_button.pack(pady=10)

    def update_doctor_password(self, username_entry, password_entry, update_password_window):
        username = username_entry.get().strip()
        new_password = password_entry.get().strip()

        if username == "" or new_password == "":
            messagebox.showerror("Error", "Please enter both username and new password.")
            return

        # Call the backend function to update the password
        if be.update_doctor_password(username, new_password):
            messagebox.showinfo("Success", f"Password for doctor '{username}' updated successfully.")
            update_password_window.destroy()
        else:
            messagebox.showerror("Error", f"Failed to update password for doctor '{username}'.")

    def delete_selected_doctor(self, doctor_listbox, delete_doctor_window):
        # Get the selected doctor's username
        selected_index = doctor_listbox.curselection()
        if selected_index:
            selected_doctor = doctor_listbox.get(selected_index)
            # Call the backend function to delete the doctor and associated patients
            deleted_doctor, deleted_patients = be.delete_doctor_with_patients(selected_doctor)
            # Display message with the deleted doctor and associated patients
            message = f"Doctor '{deleted_doctor}' and all associated patients deleted successfully."
            messagebox.showinfo("Success", message)
            # Update the listbox to reflect the deletion
            doctor_listbox.delete(selected_index)
            # Close the window after deletion
            delete_doctor_window.destroy()
            # Refresh the screen with updated data
            self.populate_patients_list()
            self.update_patient_count_label()
        else:
            messagebox.showerror("Error", "Please select a doctor to delete.")

    def add_patient(self):
        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        diagnosis = self.diagnosis_entry.get("1.0", tk.END).strip()
        if name == "" or surname == "" or diagnosis == "":
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        be.create_patient(self.doctor_id, name, surname, diagnosis)
        self.name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.diagnosis_entry.delete("1.0", tk.END)
        self.populate_patients_list()  # Refresh patient list
        self.update_patient_count_label()  # Update patient count label

    def populate_patients_list(self):
        # Clear previous entries
        self.tree.delete(*self.tree.get_children())

        # Calculate start and end indices for the current page
        start_index = (self.current_page - 1) * self.page_size
        end_index = start_index + self.page_size

        # Fetch patients from the database
        patients = be.get_patients(self.doctor_id)

        # Filter patients for the current page
        patients_on_current_page = patients[start_index:end_index]

        # Clear any previous patient IDs
        self.patient_ids = []

        # Populate the Treeview with patient data and spacing
        for i, patient in enumerate(patients_on_current_page):
            patient_id = patient[0]
            self.patient_ids.append(patient_id)
            # Ensure the order of values matches the order of columns in the Treeview
            self.tree.insert("", "end", values=(patient[2], patient[3], patient[4], patient[5]))

            # Add empty rows between data rows for spacing
            if i < len(patients_on_current_page) - 0.5:
                self.tree.insert("", "end", values=("", "", "", ""), tags=("spaced",))

        # Update patient count label to show the current page and total pages
        total_patients = len(patients)
        total_pages = (total_patients + self.page_size - 1) // self.page_size
        self.patient_count_label.config(
            text=f"Page {self.current_page}/{total_pages}, Total Patients: {total_patients}")

        # Update patient count label
        self.update_patient_count_label()

        # Update the style to adjust row height and spacing
        self.style.configure("Custom.Treeview", rowheight=25, padding=10)

    def update_patient_count_label(self):
        total_patients = len(be.get_patients(self.doctor_id))
        total_pages = (total_patients + self.page_size - 1) // self.page_size
        self.patient_count_label.config(
            text=f"Page {self.current_page}/{total_pages}, Total Patients: {total_patients}")

    def filter_patients(self):
        filter_name = self.filter_name_entry.get().strip().lower()
        filter_surname = self.filter_surname_entry.get().strip().lower()

        # Convert selected dates to the correct format if they are not None
        start_date = self.selected_start_date
        end_date = self.selected_end_date

        # Ensure that start_date and end_date are of type datetime.date
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Fetch patients based on name filter
        patients = be.get_patients_by_name(self.doctor_id, filter_name)

        # Filter patients based on surname filter
        filtered_patients = [patient for patient in patients if
                             (filter_surname in patient[3].lower() if filter_surname else True)]

        # Apply date range filter if both start date and end date are selected
        if start_date and end_date:
            # Convert selected dates to datetime objects for comparison
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.min.time())
  # Add one day to include end_date

            # Filter patients based on registration date within the selected range
            filtered_patients = [patient for patient in filtered_patients if
                                 start_datetime <= datetime.strptime(patient[5].split()[0], "%Y-%m-%d") <= end_datetime]

        # Clear previous entries
        self.tree.delete(*self.tree.get_children())

        if filtered_patients:
            # Populate the Treeview with filtered patient data
            for i, patient in enumerate(filtered_patients):
                # Ensure the order of values matches the order of columns in the Treeview
                self.tree.insert("", "end", values=(patient[2], patient[3], patient[4], patient[5]))
                # Add empty rows between data rows for spacing
                if i < len(filtered_patients) - 0.5:
                    self.tree.insert("", "end", values=("", "", "", ""), tags=("spaced",))
            message = f"Retrieved {len(filtered_patients)} patient(s) matching the criteria successfully."
        else:
            message = "No patients found matching the criteria."

        # Show message in the console
        print(message)

        # Update patient count label
        self.patient_count_label.config(text=f"Total Patients: {len(filtered_patients)}")

    def clear_filter_fields(self):
        # Clear all filter fields
        self.filter_name_entry.delete(0, tk.END)
        self.filter_surname_entry.delete(0, tk.END)
        self.selected_start_date = None
        self.selected_start_date_label.config(text="")
        self.selected_end_date = None
        self.selected_end_date_label.config(text="")
        self.populate_patients_list()  # Refresh patient list
        self.update_patient_count_label()

    def show_start_date_calendar(self):
        # Create a personalized calendar window to select the start date
        self.start_date_calendar_window = PersonalizedCalendar(self)
        self.start_date_calendar_window.title("Select Start Date")
        self.start_date_calendar_window.save_button.config(command=self.get_selected_start_date)

    def get_selected_start_date(self):
        if self.start_date_calendar_window.current_day.get():
            self.selected_start_date = "{}-{}-{}".format(self.start_date_calendar_window.current_year.get(),
                                                         self.start_date_calendar_window.current_month.get(),
                                                         self.start_date_calendar_window.current_day.get())
            self.selected_start_date_label.config(text=self.selected_start_date)
            self.start_date_calendar_window.destroy()
        else:
            messagebox.showerror("Error", "Please select a start date.")

    def show_end_date_calendar(self):
        # Create a personalized calendar window to select the end date
        self.end_date_calendar_window = PersonalizedCalendar(self)
        self.end_date_calendar_window.title("Select End Date")
        self.end_date_calendar_window.save_button.config(command=self.get_selected_end_date)

    def get_selected_end_date(self):
        if self.end_date_calendar_window.current_day.get():
            self.selected_end_date = "{}-{}-{}".format(self.end_date_calendar_window.current_year.get(),
                                                       self.end_date_calendar_window.current_month.get(),
                                                       self.end_date_calendar_window.current_day.get())
            self.selected_end_date_label.config(text=self.selected_end_date)
            self.end_date_calendar_window.destroy()
        else:
            messagebox.showerror("Error", "Please select an end date.")

    def logout(self):
        # Close the current application window
        self.destroy()

        # Open the login screen
        login_screen = LoginScreen()
        login_screen.mainloop()

    def on_tree_double_click(self, event):
        if not self.crud_window_open:
            item = self.tree.selection()
            if item:
                item = item[0]
                name = self.tree.item(item, "values")[0]
                surname = self.tree.item(item, "values")[1]
                diagnosis = self.tree.item(item, "values")[2]
                index = self.tree.index(item) // 2  # Adjust index calculation considering the spacing

                if 0 <= index < len(self.patient_ids):
                    patient_id = self.patient_ids[index]

                    # Fetch the doctor's username who added this patient
                    doctor_username = be.get_doctor_username(patient_id)

                    # Open the CRUD window with patient details
                    CRUDWindow(self, self.role, name, surname, diagnosis, patient_id, doctor_username)

                    # Set the flag to indicate that a CRUD window is open
                    self.crud_window_open = True
                else:
                    messagebox.showerror("Error", "Index out of range")
        else:
            messagebox.showwarning("Warning", "A CRUD window is already open")

    def on_crud_window_close(self, event):
        # Reset the flag when the CRUD window is closed
        self.crud_window_open = False

    def update_patient_list(self, deleted_index):
        # Remove the patient ID from the list
        del self.patient_ids[deleted_index]

        # Reindex patient IDs in the treeview
        for i in range(deleted_index, len(self.patient_ids)):
            item = self.tree.get_children()[i]
            self.tree.item(item, values=(i + 1,))


class CRUDWindow(tk.Toplevel):
    def __init__(self, master, role, name, surname, diagnosis, patient_id, doctor_username):
        super().__init__(master)
        self.selected_patient_id = None  # Initialize selected_patient_id attribute to None

        self.parent = master  # Store the parent window
        self.title("Update Patient")
        self.geometry("600x280")

        self.patient_id = patient_id
        self.role = role

        self.selected_patient_id = patient_id

        self.patient_id_label = tk.Label(self, text="Patient ID:")
        self.patient_id_entry = tk.Entry(self)
        self.patient_id_entry.insert(0, patient_id)

        self.name_label = tk.Label(self, text="Name:")
        self.name_entry = tk.Entry(self)
        self.name_entry.insert(0, name)

        self.surname_label = tk.Label(self, text="Surname:")
        self.surname_entry = tk.Entry(self)
        self.surname_entry.insert(0, surname)

        self.diagnosis_label = tk.Label(self, text="Diagnosis:")
        self.diagnosis_entry = tk.Text(self, height=5, width=60)  # Use a Text widget for diagnosis
        self.diagnosis_entry.insert(tk.END, diagnosis)

        self.doctor_username_label = tk.Label(self, text="Doctor:")
        self.doctor_username_entry = tk.Entry(self)
        self.doctor_username_entry.insert(0, doctor_username)

        self.update_button = tk.Button(self, text="Update", command=self.update_patient)
        self.delete_button = tk.Button(self, text="Delete", command=self.delete_patient)

        self.name_label.grid(row=0, column=0, sticky="e")
        self.name_entry.grid(row=0, column=1)

        self.surname_label.grid(row=1, column=0, sticky="e")
        self.surname_entry.grid(row=1, column=1)

        self.doctor_username_label.grid(row=2, column=0, sticky="e")
        self.doctor_username_entry.grid(row=2, column=1)

        self.diagnosis_label.grid(row=3, column=0, sticky="ne")  # Adjust alignment for the label
        self.diagnosis_entry.grid(row=3, column=1)

        self.update_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.delete_button.grid(row=5, column=0, columnspan=2)

        # Bind the destroy event to the method in the parent window
        self.bind("<Destroy>", master.on_crud_window_close)

    def load_data(self):
        # Call the populate_patients_list method to load data into the Treeview
        self.master.populate_patients_list()

    def update_patient(self):
        # Retrieve data from entries
        patient_id = self.patient_id_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        diagnosis = self.diagnosis_entry.get("1.0", tk.END).strip()
        role = self.role  # Access the role directly from self

        # Call the update_patient function from backend
        be.update_patient(role, patient_id, name, surname, diagnosis)

        # Destroy the window after updating
        self.destroy()
        self.load_data()

    def delete_patient(self):
        role = self.role  # Access the role directly from self
        # Assuming you have a variable storing the selected patient's ID
        patient_id_numeric = self.selected_patient_id
        be.delete_patient(patient_id_numeric, role)  # Pass role here
        # Call the populate_patients_list method of the parent window to update the patient list and count
        self.parent.populate_patients_list()
        # Call the update_patient_count_label method of the parent window to update the patient count label
        self.parent.update_patient_count_label()
        # Close the CRUD window after deletion
        self.destroy()


if __name__ == "__main__":
    # Create an instance of LoginScreen
    login_screen = LoginScreen()
    login_screen.mainloop()
