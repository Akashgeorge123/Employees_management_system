from notifications import *

leave_requests = []

def request_leave(emp_id):
    con = sqlite3.connect("EMS.db")
    cursor = con.cursor()
    
    date = input("Enter leave date (YYYY-MM-DD): ")
    reason = input("Enter reason for leave: ")
    
    cursor.execute("INSERT INTO Leaves(emp_id, date, reason, status) VALUES (?, ?, ?, ?)",
                   (emp_id, date, reason, "Pending"))
    con.commit()
    con.close()
    
    print("✅ Leave request submitted. You will be notified once the admin reviews it.")

  

def view_leave_requests():
  for idx, leave in enumerate(leave_requests, 1):
    print(f"{idx}. Emp {leave['emp_id']} | Date: {leave['date']} |"
    f"Reason: {leave['reason']} | Status: {leave['Status']}")
    

def approve_reject_leave(index, decision):
  if 0 < index <= len(leave_requests):
    leave = leave_requests[index-1]
    leave_requests[index - 1]["status"] = decision
    send_notification(leave["emp_id"], f"Your leave on {leave['date']} was {decision}", target="employee")
    print(f"Leave {decision} for Emp {leave_requests[index-1]['emp_id']}")
  else:
    print("Invalid request number")