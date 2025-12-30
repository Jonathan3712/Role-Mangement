# Setup & Execution Guide

Thank you for reviewing this project. Follow these steps to run locally.

---

## 🔧 Requirements
- Python 3.10+
- MySQL
- pip

---

## 1️⃣ Clone Repo


## 3️⃣ Database Setup

Run the database bootstrap script:

mysql -u root -p < database_setup.sql

This will:
Create database: suny
Create all required tables

Add a default admin user

You may then create new users through the Signup screen or directly via Admin panel.
