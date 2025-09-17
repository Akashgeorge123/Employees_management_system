Employee Management System (EMS)

A Python-based Employee Management System with SQLite backend to manage employees, attendance, leaves, payroll, and notifications. The system supports both Admin and Employee roles, providing secure login, account management, and automated payroll calculation.

Features
Admin

Create, view, and unlock employee accounts

Approve or reject leave requests

Finalize monthly payroll for employees

View and clear notifications

Employee

Mark attendance with automatic work-hour calculation and status

Request leaves

View and clear personal notifications

Request salary for a specific month

Common

Login via Employee ID or Email

Account locking after 5 failed login attempts (employees only)

Automatic unique 6-digit Employee ID generation

Notifications system for admin and employees










Installation

Clone the repository

git clone <repository-url>
cd EMS


Install dependencies
Python standard libraries are used (sqlite3, datetime, re), no external packages required.

Run the system

python E_M_S.py


The system will automatically create the SQLite database and tables if they don’t exist.

Usage
Login

Use either Email (e.g., admin@gmail.com) or Employee ID (6-digit)

Default Admin credentials:

Email: admin@gmail.com
Password: admin123

Admin Menu

Approve/Reject Leaves – Manage employee leave requests

Finalize Payroll – Calculate salaries based on attendance

View Notifications – See notifications sent to admins

Clear Notifications – Delete all notifications

Create Employee/Admin – Add new users

Unlock Employee Account – Unlock accounts locked due to failed login attempts

View Users – List all employees

Employee Menu

Mark Attendance – Enter check-in/out times

Request Leave – Submit leave requests

View Notifications – Check personal notifications

Clear Notifications – Delete personal notifications

View Salary – Check salary status for a month






Notes

Attendance statuses:

PR – Present (≥9 hours)

LOP – Half-day (≥4 hours)

AB – Absent (<4 hours)

Salary calculation is automated based on attendance:

PR = 1000/day, LOP = 500/day, PR+OT = 1250/day

Notifications are used for leave approvals, salary finalization, and admin alerts.