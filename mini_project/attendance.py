from datetime import datetime
import sqlite3

def mark_attendance(emp_id):
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()

    date = input("Enter date (YYYY-MM-DD): ")

    # Check if attendance already exists for this employee and date
    cursor.execute("SELECT * FROM Attendance WHERE emp_id=? AND date=?", (emp_id, date))
    if cursor.fetchone():
        print("⚠️ Attendance already marked for today.")
        con.close()
        return

    # Input check-in/check-out times
    check_in_str = input("Enter check-in time (HH:MM): ")
    check_out_str = input("Enter check-out time (HH:MM): ")

    try:
        check_in = datetime.strptime(check_in_str, "%H:%M")
        check_out = datetime.strptime(check_out_str, "%H:%M")
    except ValueError:
        print("❌ Invalid time format. Use HH:MM.")
        con.close()
        return

    # Calculate hours worked
    hours_worked = (check_out - check_in).seconds / 3600

    # Determine status
    if hours_worked >= 9:
        status = "PR"
    elif hours_worked >= 4:
        status = "LOP"
    else:
        status = "AB"

    # Insert into database
    cursor.execute("""
        INSERT INTO Attendance(emp_id, date, check_in, check_out, hours_worked, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (emp_id, date, check_in_str, check_out_str, hours_worked, status))

    con.commit()
    con.close()

    print(f"✅ Attendance marked for {date}: {hours_worked:.2f} hrs, Status: {status}")
