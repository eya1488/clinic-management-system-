import mysql.connector
import bcrypt


def project():
    try:
        conn = mysql.connector.connect(
            user="eya",
            password="admin"
        )
        cursor = conn.cursor()

        # Create the database if it does not exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS clinic_manager")
        print("Database 'clinic_manager' created or already exists.")

        conn.database = "clinic_manager"

        # Create the 'admin' table if it does not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)
        print("Table 'admin' created or already exists.")

        # Create the 'appointments' table if it does not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_name VARCHAR(100),
                doctor_name VARCHAR(100) NOT NULL,
                appointment_date DATE NOT NULL,
                appointment_time TIME NOT NULL,
                availability BOOLEAN DEFAULT TRUE,
                creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Table 'appointments' created or already exists.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        conn.close()


# Call the project function to create the database and tables
project()


def insert_admin():
    try:
        conn = mysql.connector.connect(
            user="eya",
            password="admin",
            database="clinic_manager"
        )
        cursor = conn.cursor()

        # Encrypt the password for security
        hashed_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("""
            INSERT IGNORE INTO admin (username, password)
            VALUES (%s, %s)
        """, ('admin88', hashed_password))  # admin username and encrypted password
        conn.commit()
        print("Admin account created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


# Insert an admin user for testing
insert_admin()


def connect_db():
    return mysql.connector.connect(
        user="eya",
        password="admin",
        database="clinic_manager"
    )


def add_appointment(doctor_name, appointment_date, appointment_time):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO appointments (doctor_name, appointment_date, appointment_time, availability)
            VALUES (%s, %s, %s, %s)
        """, (doctor_name, appointment_date, appointment_time, True))
        conn.commit()
        print("Appointment added successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        conn.close()


def view_appointments():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
                    SELECT * FROM appointments
                    ORDER BY availability DESC, appointment_date, appointment_time
                """)
        appointments = cursor.fetchall()
        return appointments  # Returns all rows

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        conn.close()


def update_appointment(appointment_id,doctor_name, appointment_date, appointment_time):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE appointments
            SET doctor_name = %s, appointment_date = %s, appointment_time = %s
            WHERE id = %s
        """, (doctor_name, appointment_date, appointment_time, appointment_id))
        conn.commit()
        print("Appointment updated successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        conn.close()


def delete_appointment(appointment_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Delete the appointment with the given ID
        cursor.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
        conn.commit()

        # No need to reset AUTO_INCREMENT; it will handle itself
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error deleting appointment: {e}")
        raise e

