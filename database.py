import sqlite3
import os

def create_connection():
    """Create a connection to the SQLite database."""
    if not os.path.exists('database'):
        os.makedirs('database')  # Create the folder if it doesn't exist

    conn = sqlite3.connect('database/employee_db.db')
    return conn

def create_table():
    """Create the employees table if it doesn't already exist."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employee_id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        designation TEXT,
        team TEXT,
        role TEXT,
        skills TEXT
    )
    ''')
    conn.commit()
    conn.close()

def add_employee(employee):
    """Insert a new employee record into the database or update existing employee if the employee_id already exists."""
    conn = create_connection()
    cursor = conn.cursor()

    # Check if the employee already exists based on employee_id
    cursor.execute('SELECT * FROM employees WHERE employee_id=?', (employee['employee_id'],))
    existing_employee = cursor.fetchone()

    if existing_employee:
        # If employee exists, update their data
        cursor.execute('''
        UPDATE employees 
        SET name=?, email=?, designation=?, team=?, role=?, skills=? 
        WHERE employee_id=?
        ''', (employee['name'], employee['email'], employee['designation'], employee['team'], employee['role'], employee['skills'], employee['employee_id']))
    else:
        # If employee does not exist, insert a new record
        cursor.execute('''
        INSERT INTO employees (employee_id, name, email, designation, team, role, skills) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (employee['employee_id'], employee['name'], employee['email'], employee['designation'], employee['team'], employee['role'], employee['skills']))

    conn.commit()
    conn.close()

def update_employee(employee):
    """Update an existing employee record in the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE employees SET name=?, email=?, designation=?, team=?, role=?, skills=? 
    WHERE employee_id=?
    ''', (employee['name'], employee['email'], employee['designation'], employee['team'], employee['role'], employee['skills'], employee['employee_id']))
    conn.commit()
    conn.close()

def delete_employee(employee_id):
    """Delete an employee record from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE employee_id=?', (employee_id,))
    conn.commit()
    conn.close()

def delete_all_employees():
    """Delete all employee records from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees')
    conn.commit()
    conn.close()

def get_all_employees(filter_term=""):
    """Retrieve all employee records from the database with optional filtering."""
    conn = create_connection()
    cursor = conn.cursor()

    if filter_term:
        cursor.execute('''
        SELECT * FROM employees
        WHERE employee_id LIKE ? OR name LIKE ? OR team LIKE ? OR role LIKE ? OR skills LIKE ?
        ''', ('%' + filter_term + '%', '%' + filter_term + '%', '%' + filter_term + '%', '%' + filter_term + '%', '%' + filter_term + '%'))
    else:
        cursor.execute('SELECT * FROM employees')
    
    employees = cursor.fetchall()
    conn.close()
    return employees
