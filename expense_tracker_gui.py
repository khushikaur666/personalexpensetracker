import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

DB_NAME = "expenses.db"

# database connection

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        amount REAL NOT NULL CHECK(amount > 0)
    )
    """)

    conn.commit()
    conn.close()

# functions for expenses

def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()

    if not date or not category or not amount:
        messagebox.showerror("Error", "Please fill all required fields 💗")
        return

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Amount must be a positive number 💸")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
        (date, category, description, amount),
    )
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Expense added successfully! 🎀")

    clear_fields()
    load_expenses()

def load_expenses():
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", "end", values=row)

def delete_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select an expense to delete 🗑️")
        return

    expense_id = tree.item(selected[0])["values"][0]

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Deleted", "Expense deleted successfully 💔")
    load_expenses()

def clear_fields():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# gui setup with tkinter

create_table()

root = tk.Tk()
root.title("🎀Personal Expense Tracker")
root.geometry("700x500")
root.configure(bg="#f8d7ff")

title_label = tk.Label(
    root,
    text="💖 Personal Finance Tracker 💖",
    font=("Helvetica", 18, "bold"),
    bg="#f8d7ff",
    fg="#6a0572",
)
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#f8d7ff")
frame.pack(pady=10)

# labels and entries
tk.Label(frame, text="Date (YYYY-MM-DD)", bg="#f8d7ff").grid(row=0, column=0)
date_entry = tk.Entry(frame)
date_entry.grid(row=0, column=1)

tk.Label(frame, text="Category", bg="#f8d7ff").grid(row=1, column=0)

categories = [
    "Food 🍔",
    "Transport 🚗",
    "Rent 🏠",
    "Tuition",
    "Shopping 🛍️",
    "Entertainment 🎮",
    "Other 📦"
]

category_entry = ttk.Combobox(frame, values=categories, state="readonly")
category_entry.grid(row=1, column=1)
category_entry.set("Food 🍔")

tk.Label(frame, text="Description", bg="#f8d7ff").grid(row=2, column=0)
description_entry = tk.Entry(frame)
description_entry.grid(row=2, column=1)

tk.Label(frame, text="Amount(no $ sign)", bg="#f8d7ff").grid(row=3, column=0)
amount_entry = tk.Entry(frame)
amount_entry.grid(row=3, column=1)

# buttons
add_button = tk.Button(
    root,
    text="Add Expense 💸",
    command=add_expense,
    bg="#ffb3ec",
    fg="black",
    width=20,
)
add_button.pack(pady=5)

delete_button = tk.Button(
    root,
    text="Delete Selected 🗑️",
    command=delete_expense,
    bg="#ffcce6",
    fg="black",
    width=20,
)
delete_button.pack(pady=5)

# table
columns = ("ID", "Date", "Category", "Description", "Amount")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(pady=10, fill="both", expand=True)

load_expenses()

root.mainloop()
