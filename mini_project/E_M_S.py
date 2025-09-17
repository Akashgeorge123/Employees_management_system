from database import *  
from admin import *        # approve_reject_leave(), finalize_month(), create_user(), unlock_employee(), view_users()
from attendance import *   # mark_attendance()
from leave_mgmt import *   # request_leave()
from login import *        # login()
from notifications import *  # view_notifications(), clear_notifications()
from payroll import *      # view_salary()
import sqlite3

# --- Helper ---
def get_emp_db_id(employee_id):
    """Convert 6-digit employee_id → internal emp_id"""
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()
    cursor.execute("SELECT emp_id FROM Employees WHERE employee_id=?", (employee_id,))
    row = cursor.fetchone()
    con.close()
    return row[0] if row else None

# --- Menus ---
def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Approve/Reject Leaves")
        print("2. Finalize Payroll")
        print("3. View Notifications")
        print("4. Clear Notifications")
        print("5. Create Employee/Admin")
        print("6. Unlock Employee Account")
        print("7. View Users")   # 🔥 new option
        print("8. Exit")
        try:
            c = int(input("Choice: "))
        except ValueError:
            print("⚠️ Invalid input. Enter a number.")
            continue

        if c == 1:
            approve_reject_leave()
        elif c == 2:
            employee_id = input("Enter Employee ID (6-digit) to finalize: ")
            emp_id = get_emp_db_id(employee_id)
            if not emp_id:
                print("⚠️ Employee not found.")
                continue
            month = input("Enter month (YYYY-MM): ")
            finalize_month(emp_id, month)
        elif c == 3:
            view_notifications("admin")
        elif c == 4:
            clear_notifications("admin")
        elif c == 5:
            create_user()  # this now generates employee_id automatically
        elif c == 6:
            employee_id = input("Enter Employee ID (6-digit) to unlock: ")
            emp_id = get_emp_db_id(employee_id)
            if not emp_id:
                print("⚠️ Employee not found.")
                continue
            unlock_employee(emp_id)
        elif c == 7:
            view_users()   # 🔥 call the function
        elif c == 8:
            break
        else:
            print("⚠️ Invalid choice")


def employee_menu(emp_id, emp_code):   # 🔥 added emp_code to show ID
    while True:
        print(f"\n--- Employee Menu (ID: {emp_code}) ---")   # 🔥 show employee_id
        print("1. Mark Attendance")
        print("2. Request Leave")
        print("3. View Notifications")
        print("4. Clear Notifications")
        print("5. View Salary")
        print("6. Exit")
        try:
            c = int(input("Choice: "))
        except ValueError:
            print("⚠️ Invalid input. Enter a number.")
            continue

        if c == 1:
            mark_attendance(emp_id)  # automatic status by time
        elif c == 2:
            request_leave(emp_id)
        elif c == 3:
            view_notifications("employee", emp_id)  # unread at top, option to mark as read
        elif c == 4:
            clear_notifications("employee", emp_id)  # clears only this employee's notifications
        elif c == 5:
            month = input("Enter month (YYYY-MM): ")
            request_salary(emp_id, month)
        elif c == 6:
            break
        else:
            print("⚠️ Invalid choice")

# --- Main ---
create_db()  # ensure all tables exist
while True:
    print("\n--- Login ---")
    user_input = input("Email or Employee ID (type 'exit' to quit): ")
    if user_input.lower() == "exit":
        print("Exiting EMS. Goodbye! ✓")
        break
    pwd = input("Password: ")
    user = login(user_input, pwd)   # works for both email or id

    if user:
        emp_id, emp_code, role = user   # 🔥 unpack 3 values
        if role == "Admin":
            admin_menu()
        else:
            employee_menu(emp_id, emp_code)
