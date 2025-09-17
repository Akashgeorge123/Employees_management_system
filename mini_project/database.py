import sqlite3
import random

def generate_employee_id():
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()
    while True:
        emp_code = str(random.randint(100000, 999999))
        cursor.execute("SELECT 1 FROM Employees WHERE employee_id=?", (emp_code,))
        if not cursor.fetchone():
            con.close()
            return emp_code

def create_db():
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()
    
    # Employees table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Employees(
        emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('Admin','Employee')) NOT NULL,
        failed_attempts INTEGER DEFAULT 0,
        account_locked INTEGER DEFAULT 0
    )
    """)
    
    # Add default admin if not exists
    cursor.execute("SELECT * FROM Employees WHERE role='Admin'")
    if not cursor.fetchone():
        emp_code = generate_employee_id()
        cursor.execute("""
            INSERT INTO Employees (employee_id, name, email, password, role)
            VALUES (?, ?, ?, ?, ?)
        """, (emp_code, "Admin", "admin@gmail.com", "admin123", "Admin"))
        print(f"✅ Default Admin created with Employee ID: {emp_code}")
    
    # Attendance Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER,
        date TEXT,
        check_in TEXT,
        check_out TEXT,
        hours_worked REAL,
        status TEXT,
        FOREIGN KEY(emp_id) REFERENCES Employees(emp_id)
    )
    """)
    
    # Leaves Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Leaves(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER,
        date_from TEXT,
        date_to TEXT,
        leave_type TEXT,
        reason TEXT,
        status TEXT,
        FOREIGN KEY(emp_id) REFERENCES Employees(emp_id)
    )
    """)
    
    # Notifications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Notifications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER,
        message TEXT,
        is_read INTEGER DEFAULT 0,
        FOREIGN KEY(emp_id) REFERENCES Employees(emp_id)
    )
    """)
    
    # Payroll Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Payroll(
        emp_id INTEGER,
        month TEXT,
        total REAL,
        finalized INTEGER DEFAULT 0,
        PRIMARY KEY(emp_id, month),
        FOREIGN KEY(emp_id) REFERENCES Employees(emp_id)
    )
    """)
    
    con.commit()
    con.close()
    print("📦 Database & Tables created successfully! ✓")
