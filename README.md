🧑‍💼 Employee Management System (GUI + MySQL)

A desktop application built with Python (Tkinter) and MySQL to manage employee records. It supports adding, updating, promoting, and removing employees using an intuitive graphical user interface.

🚀 Features
1.Add new employees with real-time validation
2.Update existing employee details
3.Promote employees by increasing their salary
4.Remove employees from the system
5.View all employees in a sortable table

🛠 Tech Stack   
1.Python 3.x   
2.Tkinter for GUI   
3.MySQL for data storage (employee database with employees table)   

📦 Setup Instructions
1. Clone the Repository
   https://github.com/prathamvpatil/Python_Employee_Management_GUI.git
2. Install Requirements
   Make sure you have the required Python modules:
   pip install mysql-connector-python
3. Set Up MySQL Database
   Open MySQL and run
   CREATE DATABASE employee;

USE employee;

CREATE TABLE employees (
  id VARCHAR(10) PRIMARY KEY,
  name VARCHAR(100),
  post VARCHAR(100),
  salary INT
);
Note: Update the database credentials in main2.py:
host="localhost"
user="root"
password="YourPassword"
database="employee"
4. Run the App
python main2.py


✨ TODO
Search/filter functionality
Sort by columns
Export to CSV
Authentication system

