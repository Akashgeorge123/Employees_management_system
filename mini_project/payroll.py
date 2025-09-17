from attendance import *
from notifications import *

payroll = {}

def calculate_daily_wage(status):
    if status == "PR":
        return 1000
    elif status == "LOP":
        return 500
    elif status == "PR+OT":
        return 1250
    else:  # AB or any other
        return 0

def finalize_month(emp_id, month):
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()
    
    # Fetch all attendance records for this employee in this month
    cursor.execute("""
        SELECT date, status FROM Attendance 
        WHERE emp_id=? AND date LIKE ?
    """, (emp_id, f"{month}%"))
    
    records = cursor.fetchall()  # list of tuples (date, status)
    
    total = 0
    for date, status in records:
        total += calculate_daily_wage(status)
    
    # Insert or update payroll table
    cursor.execute("""
        INSERT OR REPLACE INTO Payroll(emp_id, month, total, finalized)
        VALUES (?, ?, ?, 1)
    """, (emp_id, month, total))
    
    con.commit()
    con.close()
    
    # ✅ Send notification to employee about finalized salary
    send_notification(emp_id, f"Your salary for {month} has been finalized: ₹{total}")

    print(f"✅ Payroll finalized for Emp {emp_id} for {month}: {total}")


def view_salary(emp_id, month):
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()

    cursor.execute("""
        SELECT total, finalized FROM Payroll 
        WHERE emp_id=? AND month=?
    """, (emp_id, month))

    record = cursor.fetchone()
    if record:
        total, finalized = record
        if finalized:
            print(f"💰 Your salary for {month} is: {total}")
        else:
            print(f"⏳ Salary for {month} is under processing. You will be notified once finalized.")
    else:
        print("✅ Request received. We will notify you after admin approval.")
    
    con.close()
