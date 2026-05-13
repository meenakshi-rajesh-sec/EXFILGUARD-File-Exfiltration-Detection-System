import tkinter as tk
from tkinter import messagebox
import subprocess

# Default demo credentials
# Change these before running in a real environment
USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"

def login():
    entered_user = user_entry.get()
    entered_pass = pass_entry.get()

    if entered_user == USERNAME and entered_pass == PASSWORD:
        root.destroy()
        subprocess.call(["python", "exfilguard_gui.py"])
    else:
        messagebox.showerror("Access Denied", "Invalid username or password.")

# Login Window
root = tk.Tk()
root.title("EXFILGUARD Login")
root.geometry("300x180")
root.configure(bg="#1e1e1e")

tk.Label(
    root,
    text="EXFILGUARD",
    font=("Helvetica", 16, "bold"),
    bg="#1e1e1e",
    fg="white"
).pack(pady=10)

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack()

tk.Label(
    frame,
    text="Username:",
    bg="#1e1e1e",
    fg="white"
).grid(row=0, column=0, pady=5)

user_entry = tk.Entry(frame, width=20)
user_entry.grid(row=0, column=1, pady=5)

tk.Label(
    frame,
    text="Password:",
    bg="#1e1e1e",
    fg="white"
).grid(row=1, column=0, pady=5)

pass_entry = tk.Entry(frame, show="*", width=20)
pass_entry.grid(row=1, column=1, pady=5)

login_btn = tk.Button(
    root,
    text="🔐 Login",
    command=login,
    width=15
)

login_btn.pack(pady=10)

root.mainloop()
