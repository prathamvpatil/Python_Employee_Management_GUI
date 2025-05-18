import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import mysql.connector

# Database connection
connection = mysql.connector.connect(
    host="localhost", user="root", password="Pratham@123", database="employee"
)

# Check if employee exists
def check_employee(emp_id):
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM employees WHERE id = %s", (emp_id,))
    exists = cursor.fetchone() is not None
    cursor.close()
    return exists

# Add Employee Window
def add_employee():
    def check_id_exists(event=None):
        emp_id = entry_id.get().strip()
        if emp_id:
            if check_employee(emp_id):
                label_warning.config(text="⚠️ ID already exists!", fg="red")
                btn_submit.config(state="disabled")
            else:
                label_warning.config(text="✅ ID is available", fg="green")
                check_fields()
        else:
            label_warning.config(text="", fg="#f0f8ff")
            btn_submit.config(state="disabled")

    def check_fields(event=None):
        # Enable only if all fields are valid
        if (
            entry_id.get().strip()
            and entry_name.get().strip()
            and entry_post.get().strip()
            and entry_salary.get().strip().isdigit()
            and "already exists" not in label_warning.cget("text")
        ):
            btn_submit.config(state="normal")
        else:
            btn_submit.config(state="disabled")

    def submit():
        emp_id = entry_id.get().strip()
        name = entry_name.get().strip()
        post = entry_post.get().strip()
        salary = entry_salary.get().strip()

        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO employees (id, name, post, salary) VALUES (%s, %s, %s, %s)",
                           (emp_id, name, post, salary))
            connection.commit()
            messagebox.showinfo("Success", "Employee added successfully.")
            window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", str(err))
            connection.rollback()
        finally:
            cursor.close()

    window = tk.Toplevel(root)
    window.title("Add Employee")
    window.geometry("450x360")
    window.configure(bg="#f0f8ff")

    labels = ["ID", "Name", "Post", "Salary"]
    entries = []

    for i, text in enumerate(labels):
        tk.Label(window, text=text, bg="#f0f8ff", font=("Arial", 12)).grid(row=i, column=0, pady=10, padx=10, sticky="e")
        entry = ttk.Entry(window, width=30)
        entry.grid(row=i, column=1, pady=10)
        entry.bind("<KeyRelease>", check_fields)
        entries.append(entry)

    entry_id, entry_name, entry_post, entry_salary = entries

    entry_id.bind("<KeyRelease>", check_id_exists)

    label_warning = tk.Label(window, text="", bg="#f0f8ff", font=("Arial", 10, "bold"))
    label_warning.grid(row=1, columnspan=2)

    btn_submit = ttk.Button(window, text="Submit", command=submit)
    btn_submit.grid(row=5, columnspan=2, pady=20)
    btn_submit.config(state="disabled")

# Remove Employee
def remove_employee():
    emp_id = simpledialog.askstring("Remove Employee", "Enter Employee ID:")
    if not emp_id:
        return
    if not check_employee(emp_id):
        messagebox.showerror("Error", "Employee does not exist.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
        connection.commit()
        messagebox.showinfo("Success", "Employee removed successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))
        connection.rollback()
    finally:
        cursor.close()

# Promote Employee
def promote_employee():
    emp_id = simpledialog.askstring("Promote Employee", "Enter Employee ID:")
    if not emp_id or not check_employee(emp_id):
        messagebox.showerror("Error", "Employee not found.")
        return

    try:
        amount = float(simpledialog.askstring("Promote Employee", "Enter increase in salary:"))
        cursor = connection.cursor()
        cursor.execute("SELECT salary FROM employees WHERE id = %s", (emp_id,))
        current_salary = cursor.fetchone()[0]
        new_salary = current_salary + amount
        cursor.execute("UPDATE employees SET salary = %s WHERE id = %s", (new_salary, emp_id))
        connection.commit()
        messagebox.showinfo("Success", "Employee promoted successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        connection.rollback()
    finally:
        cursor.close()

# View Employees (Optimized with Treeview)
def display_employees():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        cursor.close()

        display = tk.Toplevel(root)
        display.title("All Employees")
        display.geometry("800x500")
        display.configure(bg="#f8faff")

        columns = ("ID", "Name", "Post", "Salary")
        tree = ttk.Treeview(display, columns=columns, show="headings", height=20)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180)

        for emp in employees:
            tree.insert("", tk.END, values=emp)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 11), rowheight=28)

        tree.pack(expand=True, fill="both", padx=20, pady=20)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

# --- Main Window ---
root = tk.Tk()
root.title("Employee Management System")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.configure(bg="#e6f2ff")

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.map("TButton",
          foreground=[('active', '#003366')],
          background=[('active', '#cce7ff')])

# Center Frame
frame = tk.Frame(root, bg="#e6f2ff")
frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame, text="Employee Management System", font=("Helvetica", 28, "bold"), bg="#e6f2ff", fg="#003366").pack(pady=30)

# Action Buttons
buttons = [
    ("Add Employee", add_employee),
    ("Remove Employee", remove_employee),
    ("Promote Employee", promote_employee),
    ("Display Employees", display_employees),
    ("Exit", root.quit),
]

for text, command in buttons:
    ttk.Button(frame, text=text, width=30, command=command).pack(pady=10)

root.mainloop()
