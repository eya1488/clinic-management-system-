import mysql.connector
from tkinter import *
from tkinter import messagebox

# Function to connect to the database
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",  # Replace with your MySQL username
        password="your_password",  # Replace with your MySQL password
        database="clinic_manager"
    )

# Function to validate admin login
def validate_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        return result is not None
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

# Admin login GUI
def admin_login():
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()

        if validate_login(username, password):
            messagebox.showinfo("Success", "Login successful!")
            root.destroy()  # Close the login window
            manage_appointments()  # Open appointment management
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    root = Tk()
    root.title("Admin Login")

    Label(root, text="Username:").pack(pady=5)
    username_entry = Entry(root)
    username_entry.pack(pady=5)

    Label(root, text="Password:").pack(pady=5)
    password_entry = Entry(root, show="*")
    password_entry.pack(pady=5)

    login_button = Button(root, text="Login", command=handle_login)
    login_button.pack(pady=10)

    root.mainloop()

# Call the login function
admin_login()



def manage_appointments():
    def fetch_appointments():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)

        for appointment in fetch_appointments():
            tree.insert("", "end", values=appointment)

    def add_appointment():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO appointments (patient_name, doctor_name, appointment_date, appointment_time, is_available)
                VALUES (%s, %s, %s, %s, TRUE)
            """, (patient_name_entry.get(), doctor_name_entry.get(), date_entry.get(), time_entry.get()))
            conn.commit()
            messagebox.showinfo("Success", "Appointment added successfully!")
            refresh_table()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")
        finally:
            cursor.close()
            conn.close()

    def delete_appointment():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to delete.")
            return

        appointment_id = tree.item(selected_item)["values"][0]

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
            conn.commit()
            messagebox.showinfo("Success", "Appointment deleted successfully!")
            refresh_table()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")
        finally:
            cursor.close()
            conn.close()

    def update_appointment():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to update.")
            return

        appointment_id = tree.item(selected_item)["values"][0]

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE appointments
                SET patient_name = %s, doctor_name = %s, appointment_date = %s, appointment_time = %s
                WHERE id = %s
            """, (patient_name_entry.get(), doctor_name_entry.get(), date_entry.get(), time_entry.get(), appointment_id))
            conn.commit()
            messagebox.showinfo("Success", "Appointment updated successfully!")
            refresh_table()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")
        finally:
            cursor.close()
            conn.close()

    # Appointment management GUI
    root = Tk()
    root.title("Appointment Management")

    # Input fields
    Label(root, text="Patient Name:").grid(row=0, column=0, padx=10, pady=5)
    patient_name_entry = Entry(root)
    patient_name_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(root, text="Doctor Name:").grid(row=1, column=0, padx=10, pady=5)
    doctor_name_entry = Entry(root)
    doctor_name_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(root, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
    date_entry = Entry(root)
    date_entry.grid(row=2, column=1, padx=10, pady=5)

    Label(root, text="Time (HH:MM:SS):").grid(row=3, column=0, padx=10, pady=5)
    time_entry = Entry(root)
    time_entry.grid(row=3, column=1, padx=10, pady=5)

    # Buttons for CRUD operations
    Button(root, text="Add Appointment", command=add_appointment).grid(row=4, column=0, padx=10, pady=10)
    Button(root, text="Update Appointment", command=update_appointment).grid(row=4, column=1, padx=10, pady=10)
    Button(root, text="Delete Appointment", command=delete_appointment).grid(row=4, column=2, padx=10, pady=10)

    # Appointment table
    tree = Treeview(root, columns=("ID", "Patient", "Doctor", "Date", "Time", "Available"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Patient", text="Patient")
    tree.heading("Doctor", text="Doctor")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Available", text="Available")
    tree.grid(row=5, column=0, columnspan=3, pady=10)

    refresh_table()

    root.mainloop()




from table_cr_ins import insert_admin
from table_cr_ins import insert_admin, connect_db
import tkinter as tk
from tkinter import messagebox
import bcrypt

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
            conn = connect_db()  # Connect to the database
            cursor = conn.cursor()

            # Check if the username exists in the admin table
            cursor.execute("SELECT password FROM admin WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result:
                # Compare the entered password with the hashed password in the database
                hashed_password = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    messagebox.showinfo("Login", "Login successful!")
                    login_window.destroy()  # Close login window


                    open_main_menu()  # Open the main menu
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

# Function to open the main menu after successful login
def open_main_menu():
    main_menu = tk.Toplevel()
    main_menu.title("Clinic Management System - Main Menu")
    tk.Label(main_menu, text="Welcome to the Clinic Management System!").pack()
    # Add buttons for CRUD operations here
    tk.Button(main_menu, text="Exit", command=main_menu.destroy).pack()

# Main Window
root = tk.Tk()
root.title("Clinic Management System")

tk.Button(root, text="Admin Login", command=admin_login_page).pack()
root.mainloop()
