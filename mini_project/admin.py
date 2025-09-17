import sqlite3,re
from database import generate_employee_id

# -------------------------
# Employee Management
# -------------------------

def unlock_employee(emp_id):
    """Unlock a locked employee account and reset failed attempts"""
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Employees WHERE emp_id=?", (emp_id,))
    if cursor.fetchone():
        cursor.execute("UPDATE Employees SET account_locked=0, failed_attempts=0 WHERE emp_id=?", (emp_id,))
        con.commit()
        print(f"✅ Employee {emp_id} unlocked successfully!")
    else:
        print("❌ Employee not found.")
    con.close()

def add_employee(name, email, password, role):
    """Add a new employee with a unique 6-digit employee_id"""
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()
    emp_code = generate_employee_id()
    try:
        cursor.execute("""
            INSERT INTO Employees(employee_id, name, email, password, role)
            VALUES (?, ?, ?, ?, ?)
        """, (emp_code, name, email, password, role))
        con.commit()
        print(f"✅ {role} '{name}' added successfully! Employee ID: {emp_code}")
    except sqlite3.IntegrityError:
        print("❌ Error: Email already exists.")
    finally:
        con.close()

def view_employees():
    """View all employees with details"""
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()
    cursor.execute("""
        SELECT emp_id, employee_id, name, email, role, account_locked FROM Employees
    """)
    rows = cursor.fetchall()
    con.close()

    if not rows:
        print("⚠️ No employees found.")
        return

    print("\n--- Employee List ---")
    for row in rows:
        print(f"ID: {row[0]}, Employee ID: {row[1]}, Name: {row[2]}, Email: {row[3]}, Role: {row[4]}, Locked: {row[5]}")

# -------------------------
# Admin Functions
# -------------------------

def create_user():
    """Admin creates a new employee or admin"""
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()

    name = input("Enter name: ").strip()

    # Email validation
    while True:
        email = input("Enter email: ").strip()
        pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
        if re.match(pattern, email):
            break
        print("⚠️ Invalid email. Must be a Gmail address.")

    # Password
    password = input("Enter password: ").strip()

    # Role selection
    while True:
        role = input("Enter role (Admin/Employee): ").strip()
        if role in ("Admin", "Employee"):
            break
        print("⚠️ Invalid role. Must be Admin or Employee.")

    # Generate employee_id
    emp_code = generate_employee_id()

    # Insert into DB
    try:
        cursor.execute("""
            INSERT INTO Employees(employee_id, name, email, password, role)
            VALUES (?, ?, ?, ?, ?)
        """, (emp_code, name, email, password, role))
        con.commit()
        print(f"✅ {role} '{name}' created successfully! Employee ID: {emp_code}")
    except sqlite3.IntegrityError:
        print("❌ Email already exists. Try again.")
    finally:
        con.close()

def view_users():
    """View all registered users (Admin view)"""
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()
    cursor.execute("SELECT employee_id, name, email, role FROM Employees")
    users = cursor.fetchall()
    con.close()

    if not users:
        print("⚠️ No users found in the system.")
        return

    print("\n--- Registered Users ---")
    for emp_code, name, email, role in users:
        print(f"🆔 {emp_code} | 👤 {name} | 📧 {email} | 🎭 {role}")
