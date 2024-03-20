# backend
import sqlite3
import tkinter.messagebox as messagebox
from datetime import datetime


def create_database_connection():
    try:
        conn = sqlite3.connect('patients.db')
        return conn
    except sqlite3.Error as err:
        print(f"Error connecting to the database: {err}")
        return None


def create_tables():
    try:
        conn = create_database_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(10) DEFAULT 'doctor'
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id INTEGER,
                name VARCHAR(255) NOT NULL,
                surname VARCHAR(255) NOT NULL,
                diagnosis TEXT NOT NULL,
                control_date TEXT NOT NULL,
                FOREIGN KEY (doctor_id) REFERENCES doctors(id)
            )
        ''')

        conn.commit()
        cursor.close()

    except sqlite3.Error as err:
        messagebox.showerror("Error", f"Error creating tables: {err}")


def execute_query(query, params=None):
    try:
        with sqlite3.connect('patients.db') as conn:

            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print(f"Error executing query: {query}")
        print(f"Error details: {e}")
        return []


def login(username, password, role=None):
    query = "SELECT id, role FROM doctors WHERE username = ? AND password = ?"
    params = (username, password)
    result = execute_query(query, params)
    if result:
        role = result[0][1]  # Extract the role retrieved from the database
        return result[0]  # Return doctor's ID and role as a tuple (ID, role)
    else:
        # Check if super user credentials are entered
        super_user_username = "admin"
        super_user_password = "17021997"  # Change this to the actual super user password
        if username == super_user_username and password == super_user_password:
            messagebox.showinfo("Success", "Login successful as admin.")
            role = 'admin'  # Set role to 'admin' for super user
            return (-1, 'admin')  # Return a unique identifier for the super user, along with the role
        else:
            return None


def register_doctor(username, password, role):
    create_tables()  # Ensure tables are created before registering a new doctor
    if not username_exists(username):
        insert_query = "INSERT INTO doctors (username, password, role) VALUES (?, ?, ?)"
        params = (username, password, role)  # Include role parameter
        execute_query(insert_query, params)
        messagebox.showinfo("Success", "Doctor registered successfully.")
        return True
    else:
        messagebox.showerror("Error", "Username already exists. Please choose another.")
        return False


def fetch_registered_doctors():
    try:
        with sqlite3.connect('patients.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM doctors")
            registered_doctors = cursor.fetchall()
            return [doctor[0] for doctor in registered_doctors]
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error fetching registered doctors: {e}")
        return []


def select_doctor_to_delete():
    registered_doctors = fetch_registered_doctors()
    if not registered_doctors:
        messagebox.showerror("Error", "No registered doctors found.")
        return None
    message = "Registered Doctors:\n"
    for i, doctor in enumerate(registered_doctors, start=1):
        message += f"{i}. {doctor}\n"
    try:
        selection = int(input("Enter the number corresponding to the doctor you want to delete: "))
        if selection < 1 or selection > len(registered_doctors):
            messagebox.showerror("Error", "Invalid selection. Please select a number from the list.")
            return None
        else:
            return registered_doctors[selection - 1]
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a number.")
        return None


def delete_doctor_with_patients(username):
    try:
        with sqlite3.connect('patients.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM doctors WHERE username = ?", (username,))
            doctor_id = cursor.fetchone()
            if doctor_id:
                doctor_id = doctor_id[0]
                cursor.execute("DELETE FROM patients WHERE doctor_id = ?", (doctor_id,))
                cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
                return username, []  # Return the deleted doctor's username and an empty list
            else:
                messagebox.showerror("Error", f"No doctor found with username '{username}'.")
                return None  # Return None when the doctor is not found
    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error deleting doctor and associated patients: " + str(e))
        return None  # Return None in case of any database error


def update_doctor_password(username, new_password):
    try:
        with sqlite3.connect('patients.db') as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE doctors SET password = ? WHERE username = ?", (new_password, username))
            if cursor.rowcount > 0:
                return True  # Password updated successfully
            else:
                messagebox.showerror("Error", f"No doctor found with username '{username}'.")
                return False  # No doctor found with the given username
    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error updating doctor password: " + str(e))
        return False  # Error updating password


def delete_selected_doctor():
    username = select_doctor_to_delete()
    if username:
        confirmation = messagebox.askquestion("Confirmation",
                                              f"Are you sure you want to delete the doctor '{username}' and all associated patients?")
        if confirmation == "yes":
            result = delete_doctor_with_patients(username)
            if result:
                pass
            else:
                messagebox.showerror("Error", f"No doctor found with username '{username}'.")
        else:
            messagebox.showinfo("Canceled", "Deletion canceled.")


def create_patient(doctor_id, name, surname, diagnosis, control_date=None):
    try:
        if control_date is None:
            control_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_query = "INSERT INTO patients (doctor_id, name, surname, diagnosis, control_date) VALUES (?, ?, ?, ?, ?)"
        params = (doctor_id, name, surname, diagnosis, control_date)
        execute_query(insert_query, params)
        messagebox.showinfo("Success", "Patient created successfully.")


    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error creating patient: {e}")


def get_patient_by_id(patient_id):
    try:
        if patient_id is not None:
            if isinstance(patient_id, int) or (isinstance(patient_id, str) and patient_id.isdigit()):
                patient_id_numeric = int(patient_id)
                select_query = "SELECT * FROM patients WHERE id = ?"
                params = (patient_id_numeric,)
                result = execute_query(select_query, params)
                if result:
                    return result[0]  # Return patient information if found
                else:
                    return None
            else:
                messagebox.showerror("Error", f"Invalid patient ID format: {patient_id}")
                return None
        else:
            return None
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error retrieving patient by ID: {e}")
        return None


def delete_patient(patient_id_numeric, role):
    try:
        if role == 'admin':
            # Check if the user has permission to delete patients
            patient = get_patient_by_id(patient_id_numeric)
            if patient:
                confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this patient?")
                if confirmation:
                    delete_query = "DELETE FROM patients WHERE id = ?"
                    params = (patient_id_numeric,)
                    execute_query(delete_query, params)
                    messagebox.showinfo("Success", "Patient deleted successfully.")
            else:
                messagebox.showerror("Error", "Patient does not exist.")
        else:
            messagebox.showerror("Error",
                                 "You do not have permission to delete patients. Only admin users can delete patients.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error deleting patient: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def update_patient(role, patient_id, name, surname, diagnosis):
    try:
        if role == 'admin':
            update_query = "UPDATE patients SET name = ?, surname = ?, diagnosis = ? WHERE id = ?"
            params = (name, surname, diagnosis, patient_id)
            execute_query(update_query, params)
            messagebox.showinfo("Success", "Patient information updated successfully.")
        else:
            messagebox.showerror("Error",
                                 "You do not have permission to update patients. Only admin users can delete patients.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error updating patient: {e}")


def get_doctor_name(doctor_id):
    if doctor_id == -1:  # Check if the ID is for the super user
        return "admin"
    else:
        query = "SELECT username FROM doctors WHERE id = ?"
        params = (doctor_id,)
        result = execute_query(query, params)
        if result:
            return result[0][0]  # Return the username of the doctor
        else:
            return None


def get_doctor_username(patient_id):
    try:
        select_query = "SELECT doctors.username FROM patients JOIN doctors ON patients.doctor_id = doctors.id WHERE patients.id = ?"
        params = (patient_id,)
        result = execute_query(select_query, params)
        if result:
            return result[0][0]  # Return the doctor's username
        else:
            return None
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error retrieving doctor's username: {e}")
        return None


def get_patients(doctor_id, start=0, end=None):
    try:
        if doctor_id == -1:  # Super user, retrieve all patients
            select_query = "SELECT * FROM patients"
            patients = execute_query(select_query)
        else:
            select_query = "SELECT * FROM patients WHERE doctor_id = ?"
            params = (doctor_id,)
            patients = execute_query(select_query, params)

        if end is None:
            return patients[start:]  # Return all patients from start_index to the end
        else:
            return patients[start:end]  # Return patients from start_index to end_index
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error retrieving patients: {e}")
        return []

def get_patients_added_today(doctor_id):
    try:
        # Get today's date and time
        today_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract date part only
        today_date = today_datetime.split()[0]

        # Query for patients added today by the specified doctor(s)
        if doctor_id == -1:
            # Fetch patients added by all doctors
            select_query = "SELECT * FROM patients WHERE control_date >= ? || ' 00:00:00' AND control_date <= ? || ' 23:59:59'"
            params = (today_date, today_date)
        else:
            # Fetch patients added today by the specified doctor
            select_query = "SELECT * FROM patients WHERE doctor_id = ? AND control_date >= ? || ' 00:00:00' AND control_date <= ? || ' 23:59:59'"
            params = (doctor_id, today_date, today_date)

        results = execute_query(select_query, params)

        # Count the number of patients added today
        today_patients_count = len(results)

        return results, today_patients_count
    except Exception as e:
        print(f"Error retrieving patients added today: {e}")
        return [], 0

def get_patients_added_today_all():
    try:
        # Get today's date and time
        today_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract date part only
        today_date = today_datetime.split()[0]

        # Query for patients added today by all doctors
        select_query = "SELECT * FROM patients WHERE control_date >= ? || ' 00:00:00' AND control_date <= ? || ' 23:59:59'"
        params = (today_date, today_date)
        results = execute_query(select_query, params)

        # Count the number of patients added today
        today_patients_count = len(results)

        return results, today_patients_count
    except Exception as e:
        print(f"Error retrieving patients added today: {e}")
        return [], 0

def get_patients_by_date_range(doctor_id, start_date, end_date, start=0, end=None):
    try:
        select_query = "SELECT * FROM patients WHERE doctor_id = ? AND control_date BETWEEN ? AND ?"
        params = (doctor_id, start_date + " 00:00:00", end_date + " 23:59:59")  # Adjust the time range
        print("Executing SQL query:")
        print("Query:", select_query)
        print("Parameters:", params)
        results = execute_query(select_query, params)
        if end is None:
            return results[start:]
        else:
            return results[start:end]
    except Exception as e:
        print(f"Error retrieving patients by date range: {e}")
        return []


def get_patients_by_date_range_and_name(doctor_id, start_date, end_date, name, start=0, end=None):
    select_query = "SELECT * FROM patients WHERE doctor_id = ? AND control_date BETWEEN ? AND ? AND (name LIKE ? OR surname LIKE ?)"
    params = (doctor_id, start_date, end_date, f"%{name}%", f"%{name}%")

    print("Executing SQL query:")
    print("Query:", select_query)
    print("Parameters:", params)

    results = execute_query(select_query, params)
    if end is None:
        return results[start:]
    else:
        return results[start:end]


def get_patients_by_name(doctor_id, name, start=0, end=None):
    try:
        if doctor_id == -1:
            select_query = "SELECT * FROM patients WHERE name LIKE ? OR surname LIKE ?"
            params = (f"%{name}%", f"%{name}%")
        else:
            select_query = "SELECT * FROM patients WHERE doctor_id = ? AND (name LIKE ? OR surname LIKE ?)"
            params = (doctor_id, f"%{name}%", f"%{name}%")
        results = execute_query(select_query, params)
        if end is None:
            return results[start:]
        else:
            return results[start:end]
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error retrieving patients by name: {e}")
        return []


def get_all_patients(start=0, end=None):
    try:
        select_query = "SELECT * FROM patients"
        results = execute_query(select_query)
        if end is None:
            return results[start:]
        else:
            return results[start:end]
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error retrieving all patients: {e}")
        return []


def username_exists(username):
    query = "SELECT id FROM doctors WHERE username = ?"
    params = (username,)
    result = execute_query(query, params)
    if result:
        return True

    else:
        return False
