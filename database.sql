-- Create database
CREATE DATABASE IF NOT EXISTS suny;
USE suny;

-- Users & roles table
CREATE TABLE IF NOT EXISTS LogIn_Credential (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'SE', 'HR', 'PR', 'General') NOT NULL
);

-- Software Engineering data
CREATE TABLE IF NOT EXISTS SE_Data (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    projectname VARCHAR(255) NOT NULL,
    supervisor VARCHAR(100) NOT NULL,
    deadline DATE NOT NULL
);

-- Software Engineering employees
CREATE TABLE IF NOT EXISTS Emp_SE (
    id INT PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    phone_no VARCHAR(20) NOT NULL,
    salary DECIMAL(10,2) NOT NULL,
    bloodgroup VARCHAR(10) NOT NULL
);

-- Human Resources data
CREATE TABLE IF NOT EXISTS HR_data (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    supervisor VARCHAR(100) NOT NULL
);

-- Human Resources employees
CREATE TABLE IF NOT EXISTS Emp_HR (
    id INT PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    phone_no VARCHAR(20) NOT NULL,
    emp_rank VARCHAR(50) NOT NULL
);

-- Payroll data
CREATE TABLE IF NOT EXISTS PR_Data (
    id INT PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    dob DATE NOT NULL
);

-- Payroll employees
CREATE TABLE IF NOT EXISTS Emp_PR (
    id INT PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    phone_no VARCHAR(20) NOT NULL,
    salary DECIMAL(10,2) NOT NULL
);

-- Optional: seed an Admin user for quick testing
INSERT INTO LogIn_Credential (username, password, role)
VALUES ('admin', 'admin123', 'Admin')
ON DUPLICATE KEY UPDATE username = username;
