from table_cr_ins import insert_admin, connect_db, add_appointment, view_appointments, update_appointment, delete_appointment
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import bcrypt
from datetime import datetime


# Function to open the admin login page
def admin_login_page():
    login_window = tk.Toplevel()
    login_window.title("Admin Login")
    tk.Label(login_window, text="Username").grid(row=0, column=0)
    tk.Label(login_window, text="Password").grid(row=1, column=0)

    username_entry = tk.Entry(login_window)
    password_entry = tk.Entry(login_window, show="*")
    username_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)

    def verify_login():
        username = username_entry.get()
        password = password_entry.get()

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Verify username and password
            cursor.execute("SELECT password FROM admin WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result:
                hashed_password = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    messagebox.showinfo("Login", "Login successful!")
                    login_window.destroy()
                    open_main_menu()  # Open main menu
                else:
                    messagebox.showerror("Login", "Incorrect password.")
            else:
                messagebox.showerror("Login", "Username not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            cursor.close()
            conn.close()

    tk.Button(login_window, text="Login", command=verify_login).grid(row=2, column=1)
    login_window.mainloop()


# Main Menu with "View Appointments" Button
def open_main_menu():
    main_menu = tk.Toplevel()
    main_menu.title("Clinic Management System - Main Menu")

    tk.Label(main_menu, text="Welcome to the Clinic Management System!").pack()

    # View Appointments button
    tk.Button(main_menu, text="View Appointments", command=view_appointments_gui).pack()


def view_appointments_gui():
    view_window = tk.Toplevel()
    view_window.title("View Appointments")

    # Table to display appointments
    columns = ("ID", "Patient Name", "Doctor Name", "Date", "Time")  # Removed "Available" and "Created On"
    tree = ttk.Treeview(view_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)

    tree.pack()

    def refresh_tree():
        """Refresh the Treeview with the latest appointment data."""
        # Clear existing rows
        for row in tree.get_children():
            tree.delete(row)

        # Fetch updated data from the database
        appointments = view_appointments()
        for appointment in appointments:
            tree.insert("", "end", values=appointment[:-2])  # Exclude last two columns

    # Initial population of the Treeview
    refresh_tree()

    # Buttons for CRUD operations
    tk.Button(view_window, text="Add Appointment", command=lambda: add_appointment_gui(refresh_tree)).pack()
    tk.Button(view_window, text="Update Appointment", command=lambda: update_appointment_gui(refresh_tree)).pack()
    tk.Button(view_window, text="Delete Appointment", command=lambda: delete_appointment_gui(refresh_tree)).pack()


# GUI for adding an appointment
def add_appointment_gui(refresh_tree):
    add_window = tk.Toplevel()
    add_window.title("Add Appointment")

    tk.Label(add_window, text="Patient Name").grid(row=0, column=0)
    tk.Label(add_window, text="Doctor Name").grid(row=1, column=0)
    tk.Label(add_window, text="Appointment Date (YYYY-MM-DD)").grid(row=2, column=0)
    tk.Label(add_window, text="Appointment Time (HH:MM:SS)").grid(row=3, column=0)

    patient_name_entry = tk.Entry(add_window)
    doctor_name_entry = tk.Entry(add_window)
    appointment_date_entry = tk.Entry(add_window)
    appointment_time_entry = tk.Entry(add_window)

    patient_name_entry.grid(row=0, column=1)
    doctor_name_entry.grid(row=1, column=1)
    appointment_date_entry.grid(row=2, column=1)
    appointment_time_entry.grid(row=3, column=1)

    def add_appointment_action():
        patient_name = patient_name_entry.get()
        doctor_name = doctor_name_entry.get()
        appointment_date = appointment_date_entry.get()
        appointment_time = appointment_time_entry.get()

        try:
            # Validate time format
            datetime.strptime(appointment_time, "%H:%M:%S")  # Raises ValueError if format is incorrect

            add_appointment(patient_name, doctor_name, appointment_date, appointment_time)
            messagebox.showinfo("Success", "Appointment added successfully!")
            refresh_tree()  # Refresh the appointments list
            add_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Use HH:MM:SS.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add appointment: {e}")

    tk.Button(add_window, text="Add Appointment", command=add_appointment_action).grid(row=4, column=1)


# GUI for updating an appointment
def update_appointment_gui(refresh_tree):
    update_window = tk.Toplevel()
    update_window.title("Update Appointment")

    tk.Label(update_window, text="Appointment ID").grid(row=0, column=0)
    tk.Label(update_window, text="Patient Name").grid(row=1, column=0)
    tk.Label(update_window, text="Doctor Name").grid(row=2, column=0)
    tk.Label(update_window, text="Appointment Date (YYYY-MM-DD)").grid(row=3, column=0)
    tk.Label(update_window, text="Appointment Time (HH:MM:SS)").grid(row=4, column=0)

    id_entry = tk.Entry(update_window)
    patient_name_entry = tk.Entry(update_window)
    doctor_name_entry = tk.Entry(update_window)
    appointment_date_entry = tk.Entry(update_window)
    appointment_time_entry = tk.Entry(update_window)

    id_entry.grid(row=0, column=1)
    patient_name_entry.grid(row=1, column=1)
    doctor_name_entry.grid(row=2, column=1)
    appointment_date_entry.grid(row=3, column=1)
    appointment_time_entry.grid(row=4, column=1)

    def update_appointment_action():
        appointment_id = id_entry.get()
        patient_name = patient_name_entry.get()
        doctor_name = doctor_name_entry.get()
        appointment_date = appointment_date_entry.get()
        appointment_time = appointment_time_entry.get()

        try:
            update_appointment(appointment_id, patient_name, doctor_name, appointment_date, appointment_time)
            messagebox.showinfo("Success", "Appointment updated successfully!")
            refresh_tree()  # Refresh the appointments list
            update_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update appointment: {e}")

    tk.Button(update_window, text="Update Appointment", command=update_appointment_action).grid(row=5, column=1)


# GUI for deleting an appointment
def delete_appointment_gui(refresh_tree):
    delete_window = tk.Toplevel()
    delete_window.title("Delete Appointment")

    tk.Label(delete_window, text="Appointment ID").grid(row=0, column=0)
    id_entry = tk.Entry(delete_window)
    id_entry.grid(row=0, column=1)

    def delete_appointment_action():
        appointment_id = id_entry.get()

        try:
            delete_appointment(appointment_id)
            messagebox.showinfo("Success", "Appointment deleted successfully!")
            refresh_tree()  # Refresh the appointments list
            delete_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete appointment: {e}")

    tk.Button(delete_window, text="Delete Appointment", command=delete_appointment_action).grid(row=1, column=1)


# Main Window
root = tk.Tk()
root.title("Clinic Management System")

tk.Button(root, text="Admin Login", command=admin_login_page).pack()
root.mainloop()
