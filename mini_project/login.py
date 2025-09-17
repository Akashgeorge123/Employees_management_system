import sqlite3
import re   # for email / id check

def login(user_input, password):
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()

    # Decide if input is employee_id (6 digits) or email
    if re.fullmatch(r"\d{6}", user_input):   # exactly 6 digits
        cursor.execute("SELECT emp_id, employee_id, password, role, account_locked, failed_attempts FROM Employees WHERE employee_id=?", (user_input,))
    else:  # assume it's an email
        cursor.execute("SELECT emp_id, employee_id, password, role, account_locked, failed_attempts FROM Employees WHERE email=?", (user_input,))

    row = cursor.fetchone()

    if not row:
        print("❌ User not found.")
        return None

    emp_id, emp_code, db_password, role, account_locked, failed_attempts = row

    # Admin bypasses lock
    if role != "Admin" and account_locked:
        print("⚠️ Account is locked due to multiple failed attempts.")
        con.close()
        return None

    if password == db_password:
        # Reset failed attempts for employees after successful login
        if role != "Admin":
            cursor.execute("UPDATE Employees SET failed_attempts=0 WHERE emp_id=?", (emp_id,))
            con.commit()
        print(f"✅ Login successful! Welcome {role}.")
        print(f"🆔 Your Employee ID: {emp_code}")  # show employee id
        con.close()
        return (emp_id, emp_code, role)   # 🔥 always return 3 values
    else:
        if role != "Admin":
            failed_attempts += 1
            cursor.execute("UPDATE Employees SET failed_attempts=? WHERE emp_id=?", (failed_attempts, emp_id))
            if failed_attempts >= 5:
                cursor.execute("UPDATE Employees SET account_locked=1 WHERE emp_id=?", (emp_id,))
                print("⚠️ Account locked due to 5 failed attempts!")
            else:
                print(f"❌ Wrong password! Attempt {failed_attempts}/5")
            con.commit()
        else:
            print("❌ Wrong password!")
        con.close()
        return None
