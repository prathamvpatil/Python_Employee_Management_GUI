import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector

# --- Database Functions ---
def connect_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="Pratham@123", database="employee"
    )

def fetch_all_employees():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    records = cursor.fetchall()
    conn.close()
    return records

def check_employee(emp_id):
    conn = connect_db()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM employees WHERE id = %s", (emp_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def insert_employee(emp_id, name, post, salary):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (id, name, post, salary) VALUES (%s, %s, %s, %s)",
                   (emp_id, name, post, salary))
    conn.commit()
    conn.close()

def remove_employee_db(emp_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
    conn.commit()
    conn.close()

def update_employee(emp_id, name, post, salary):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE employees SET name = %s, post = %s, salary = %s WHERE id = %s",
                   (name, post, salary, emp_id))
    conn.commit()
    conn.close()

def promote_employee_db(emp_id, increase):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT salary FROM employees WHERE id = %s", (emp_id,))
    current_salary = cursor.fetchone()[0]
    new_salary = current_salary + increase
    cursor.execute("UPDATE employees SET salary = %s WHERE id = %s", (new_salary, emp_id))
    conn.commit()
    conn.close()

# --- GUI Functions ---
def refresh_table():
    for i in tree.get_children():
        tree.delete(i)
    for row in fetch_all_employees():
        tree.insert("", tk.END, values=row)

def show_add_employee():
    popup = tk.Toplevel(root)
    popup.title("Add Employee")

    labels = ["ID", "Name", "Post", "Salary"]
    entries = []
    for label in labels:
        row = tk.Frame(popup)
        tk.Label(row, text=label+":", width=10).pack(side=tk.LEFT)
        ent = ttk.Entry(row, width=30)
        ent.pack(side=tk.LEFT)
        row.pack(pady=5)
        entries.append(ent)

    status = tk.Label(popup, text="", fg="red")
    status.pack()

    def check_id_and_update_status(emp_id):
        if check_employee(emp_id):
            status.config(text="ID already exists!", fg="red")
        else:
            status.config(text="", fg="red")

    def on_id_entry_change(event):
        emp_id = entries[0].get().strip()
        check_id_and_update_status(emp_id)

    entries[0].bind("<KeyRelease>", on_id_entry_change) # Bind to ID entry

    def validate_and_add():
        emp_id, name, post, salary = [e.get().strip() for e in entries]
        if not emp_id or not name or not post or not salary.isdigit():
            status.config(text="Please enter valid details.", fg="red")
            return
        if check_employee(emp_id):
            status.config(text="ID already exists!", fg="red")
            return
        insert_employee(emp_id, name, post, salary)
        messagebox.showinfo("Success", "Employee added.")
        popup.destroy()
        refresh_table()

    ttk.Button(popup, text="Submit", command=validate_and_add).pack(pady=10)

def show_update_employee():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Select an employee to update.")
        return

    emp_data = tree.item(selected[0], "values")
    emp_id = emp_data[0]

    popup = tk.Toplevel(root)
    popup.title("Update Employee")

    labels = ["Name", "Post", "Salary"]
    entries = []
    values = emp_data[1:]  # Skip ID

    for i, label in enumerate(labels):
        row = tk.Frame(popup)
        tk.Label(row, text=label+":", width=10).pack(side=tk.LEFT)
        ent = ttk.Entry(row, width=30)
        ent.insert(0, values[i])
        ent.pack(side=tk.LEFT)
        row.pack(pady=5)
        entries.append(ent)

    def save_updates():
        name, post, salary = [e.get().strip() for e in entries]
        if not name or not post or not salary.isdigit():
            messagebox.showerror("Error", "Enter valid details.")
            return
        update_employee(emp_id, name, post, salary)
        messagebox.showinfo("Success", "Employee updated.")
        popup.destroy()
        refresh_table()

    ttk.Button(popup, text="Save Changes", command=save_updates).pack(pady=10)

def show_promote_employee():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Select an employee to promote.")
        return

    emp_data = tree.item(selected[0], "values")
    emp_id = emp_data[0]

    try:
        amount = simpledialog.askfloat("Promote", "Enter increase in salary:")
        if amount is None or amount <= 0:
            return
        promote_employee_db(emp_id, amount)
        messagebox.showinfo("Success", "Employee promoted.")
        refresh_table()
    except:
        messagebox.showerror("Error", "Invalid amount.")

def show_remove_employee():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Select an employee to remove.")
        return
    emp_data = tree.item(selected[0], "values")
    emp_id = emp_data[0]

    if messagebox.askyesno("Confirm", f"Remove employee ID {emp_id}?"):
        remove_employee_db(emp_id)
        messagebox.showinfo("Removed", "Employee removed.")
        refresh_table()

# --- App Setup ---
root = tk.Tk()
root.title("Employee Management System")
root.geometry("1000x600")

# Sidebar
sidebar = tk.Frame(root, bg="#003366", width=200)
sidebar.pack(fill='y', side='left')

tk.Label(sidebar, text="Menu", bg="#003366", fg="white", font=("Arial", 16, "bold")).pack(pady=20)

nav_buttons = [
    ("➕ Add Employee", show_add_employee),
    ("✏️ Update Employee", show_update_employee),
    ("📈 Promote", show_promote_employee),
    ("❌ Remove", show_remove_employee),
    ("🚪 Exit", root.quit)
]

for text, cmd in nav_buttons:
    ttk.Button(sidebar, text=text, command=cmd).pack(fill='x', padx=10, pady=5)

# Content
content_frame = tk.Frame(root, bg="#f0f0f0")
content_frame.pack(expand=True, fill='both')

tk.Label(content_frame, text="Employee Records", font=("Arial", 16)).pack(pady=10)

cols = ("ID", "Name", "Post", "Salary")
tree = ttk.Treeview(content_frame, columns=cols, show='headings', height=20)
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
tree.pack(expand=True, fill='both', padx=20, pady=10)

refresh_table()

root.mainloop()