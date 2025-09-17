import sqlite3

def send_notification(emp_id=None, message="", target="employee"):
    """
    Send a notification.
    - For employees: emp_id is required.
    - For admin: emp_id=None and target='admin' will notify all admins.
    """
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()

    if target == "admin" and emp_id is None:
        cursor.execute("SELECT emp_id FROM Employees WHERE role='Admin'")
        admins = cursor.fetchall()
        for admin_id, in admins:
            cursor.execute("INSERT INTO Notifications(emp_id, message, is_read) VALUES (?, ?, 0)",
                           (admin_id, message))
    else:
        cursor.execute("INSERT INTO Notifications(emp_id, message, is_read) VALUES (?, ?, 0)",
                       (emp_id, message))

    con.commit()
    con.close()


def view_notifications(role, emp_id=None):
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()

    if role.lower() == "admin":
        # Show notifications assigned to any admin
        cursor.execute("""
            SELECT id, message, is_read FROM Notifications 
            WHERE emp_id IN (SELECT emp_id FROM Employees WHERE role='Admin')
            ORDER BY is_read ASC, id DESC
        """)
    else:
        cursor.execute("""
            SELECT id, message, is_read FROM Notifications 
            WHERE emp_id=? ORDER BY is_read ASC, id DESC
        """, (emp_id,))

    rows = cursor.fetchall()
    if not rows:
        print("📭 No notifications found.")
        con.close()
        return

    print("\n--- Notifications ---")
    for n_id, msg, is_read in rows:
        status = "🔹 Unread" if is_read == 0 else "✅ Read"
        print(f"[{status}] ({n_id}) {msg}")

    if role.lower() != "admin":
        while True:
            mark_read = input("\nMark a notification as read? Enter ID (or 'n' to skip): ").lower()
            if mark_read == 'n':
                break
            try:
                notif_id = int(mark_read)
                cursor.execute("UPDATE Notifications SET is_read=1 WHERE id=? AND emp_id=?", (notif_id, emp_id))
                con.commit()
                print(f"✅ Notification {notif_id} marked as read.")
            except ValueError:
                print("⚠️ Enter a valid notification ID.")

    con.close()


def clear_notifications(role, emp_id=None):
    """Clear notifications."""
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()

    if role.lower() == "admin":
        confirm = input("⚠️ Are you sure you want to delete ALL notifications? (y/n): ").lower()
        if confirm == "y":
            cursor.execute("DELETE FROM Notifications")
            con.commit()
            print("✅ All notifications cleared.")
        else:
            print("Operation cancelled.")
    else:
        confirm = input("⚠️ Are you sure you want to clear your notifications? (y/n): ").lower()
        if confirm == "y":
            cursor.execute("DELETE FROM Notifications WHERE emp_id=?", (emp_id,))
            con.commit()
            print("✅ Your notifications cleared.")
        else:
            print("Operation cancelled.")

    con.close()


def request_salary(emp_id, month):
    """
    Employee requests salary for a month.
    Admin will get notified.
    """
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()

    # Check if payroll record exists
    cursor.execute("SELECT * FROM Payroll WHERE emp_id=? AND month=?", (emp_id, month))
    if cursor.fetchone():
        print("✅ Salary request already exists for this month.")
        con.close()
        return

    # Insert placeholder record with finalized=0
    cursor.execute("INSERT INTO Payroll(emp_id, month, total, finalized) VALUES (?, ?, ?, ?)",
                   (emp_id, month, 0, 0))
    con.commit()
    con.close()

    # Notify all admins
    send_notification(emp_id=None, message=f"Employee ID {emp_id} requested salary for {month}", target="admin")
    print("✅ Salary request submitted. Admin will be notified.")
