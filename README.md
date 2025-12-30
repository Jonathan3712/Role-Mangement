# Role Management & Employee Operations System  
A full-stack Role-Based Access Control (RBAC) and Employee Management platform built using **Flask, MySQL, HTML/CSS, and Jinja templates**.  
This project allows organizations to manage **multiple user roles**, perform **authentication**, and execute **secure CRUD operations** across Software Engineering, HR, and Payroll departments.

---

## 🚀 Key Features
### 🔐 Authentication & Authorization
- Secure Signup & Login
- Session-based authentication
- Role-Based Dashboard Access
- Restricted route access depending on user privilege

### 🧑‍💼 Multi-Role System
Supports:
- Admin
- HR
- PR (Payroll)
- SE (Software Engineer)
- General User

Each role receives appropriate capabilities.

---

## 📋 Functional Capabilities
### 👨‍💻 Admin
- Add/Update/Delete: HR, PR, SE, and General users
- View all records
- Modify User Roles

### 🏢 HR
- Manage HR employees
- Manage Payroll employees
- View SE & PR data

### 💰 Payroll (PR)
- Manage Payroll employees & records
- View SE & HR employee data

### 💻 Software Engineer (SE)
- Manage SE employees
- Add project information
- CRUD SE tasks and data

### 🙍 General User
- Read-only access to employee records where permitted

---

## 🏗️ Tech Stack
### Backend
- Python Flask
- MySQL
- Flask Sessions
- Flask Flash Messaging

### Frontend
- HTML / CSS
- Jinja Templates
- Bootstrap (UI elements)

---

## 🧰 System Architecture


🗄️ Database Schema & Setup

This project uses MySQL to manage authentication, roles, and employee data across SE, HR, and Payroll departments.
A complete database schema is included in the project as:
database_setup.sql

This script:
Creates the database suny
Creates all required tables
Ensures structure exactly matches the Flask app
Seeds a default Admin user for quick access

▶️ Initialize Database
Make sure MySQL is installed and running.
Run this in project root:

mysql -u root -p < database_setup.sql

Or open the file in MySQL Workbench and execute.

🔐 Default Credentials

Once DB is created, you can immediately log in using:
Username: admin / root
Password: admin123 / Admin@3712
Admins have full access to all CRUD operations and role management.
