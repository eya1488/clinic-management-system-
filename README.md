# Clinic Management System

A simple clinic management system built with Python and tkinter that allows administrators to manage patient appointments efficiently.

## Features

- Secure admin login system with bcrypt password hashing
- Appointment management:
  - Add new appointments
  - View all appointments in a tabular format
  - Update existing appointments
  - Delete appointments
- User-friendly graphical interface
- MySQL database integration for persistent data storage

## Prerequisites

- Python 3.x
- MySQL Server
- Required Python packages:
  ```
  mysql-connector-python
  bcrypt
  tkinter (usually comes with Python)
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone [your-repository-url]
   cd clinic-management-system
   ```

2. Install the required packages:
   ```bash
   pip install mysql-connector-python bcrypt
   ```

3. Configure MySQL connection:
   - Open `table_cr_ins.py`
   - Update the MySQL connection parameters:
     ```python
     user="your_username"
     password="your_password"
     ```

4. Run the setup script to create the database and tables:
   ```bash
   python table_cr_ins.py
   ```

## Usage

1. Start the application:
   ```bash
   python logingui.py
   ```

2. Login using these default admin credentials:
   - Username: admin88
   - Password: admin123

3. Use the main menu to:
   - View all appointments
   - Add new appointments
   - Update existing appointments
   - Delete appointments

## File Structure

- `logingui.py`: Main application GUI and appointment management interface
- `table_cr_ins.py`: Database initialization and CRUD operations

## Database Schema

### Admin Table
- username (VARCHAR(50)) - UNIQUE
- password (VARCHAR(255))

### Appointments Table
- id (INT) - Primary Key, Auto Increment
- patient_name (VARCHAR(100))
- doctor_name (VARCHAR(100))
- appointment_date (DATE)
- appointment_time (TIME)
- availability (BOOLEAN)
- creation_date (TIMESTAMP)

## Security Features

- Password hashing using bcrypt
- Secure database connections
- Input validation for appointments

