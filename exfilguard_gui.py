import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import json
import os
from PIL import Image, ImageTk
import subprocess
import signal

USERS_FILE = "users.json"

# Default admin password
# Change this before deployment
ADMIN_PASSWORD = "YOUR_ADMIN_PASSWORD"

# ----------------- USER MANAGEMENT -----------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def create_account(username, password, admin_pass):

    users = load_users()

    if admin_pass != ADMIN_PASSWORD:
        messagebox.showerror("Error", "Invalid Admin Password!")
        return

    if username in users:
        messagebox.showerror("Error", "User already exists!")
        return

    users[username] = password

    save_users(users)

    messagebox.showinfo("Success", f"Account created for {username}!")

def login(username, password, root):

    users = load_users()

    if username in users and users[username] == password:

        messagebox.showinfo("Login Success", f"Welcome {username}!")

        root.destroy()

        launch_main_gui()

    else:
        messagebox.showerror("Error", "Invalid Username or Password!")

# ----------------- MAIN GUI -----------------
def launch_main_gui():

    global_root = tk.Tk()

    global_root.title("EXFILGUARD Control Panel")
    global_root.geometry("900x700")
    global_root.configure(bg="#1e1e1e")

    monitor_process = None
    last_read_line = 0

    # Background Image with auto-resize
    bg_label = None
    bg_img_original = None
    bg_photo = None

    def start_monitoring():

        nonlocal monitor_process

        if monitor_process is None:

            try:
                monitor_process = subprocess.Popen(
                    ["sudo", "venv/bin/python", "feds_main.py"]
                )

                status_label.config(
                    text="🟢 Monitoring Started - Tracking: Created, Modified, Deleted, Moved, Renamed, Copied"
                )

            except Exception as e:
                status_label.config(text=f"Start error: {e}")

        else:
            status_label.config(text="⚠ Already Running")

    def stop_monitoring():

        nonlocal monitor_process

        if monitor_process is not None:

            entered_pass = simpledialog.askstring(
                "Authentication Required",
                "Enter Admin Password to stop monitoring:",
                show="*",
                parent=global_root
            )

            if entered_pass != ADMIN_PASSWORD:
                messagebox.showerror("Error", "Invalid Admin Password!")
                return

            try:
                os.kill(monitor_process.pid, signal.SIGTERM)

                status_label.config(text="🔴 Monitoring Stopped")

            except Exception as e:
                status_label.config(text=f"Error stopping: {e}")

            monitor_process = None

        else:
            status_label.config(text="⚠ Not Running")

    def view_logs():

        try:
            with open("feds.log", "r") as f:

                log_text.delete(1.0, tk.END)

                log_text.insert(tk.END, f.read())

        except FileNotFoundError:

            log_text.delete(1.0, tk.END)

            log_text.insert(tk.END, "No log file found.")

    def export_logs():

        try:
            with open("feds.log", "r") as original, open(
                "exported_feds_log.txt", "w"
            ) as export:

                export.write(original.read())

            messagebox.showinfo(
                "Export Success",
                "Logs exported to exported_feds_log.txt"
            )

            status_label.config(text="✅ Logs exported successfully")

        except Exception as e:
            status_label.config(text=f"Export error: {e}")

    def clear_logs():

        result = messagebox.askyesno(
            "Confirm Clear",
            "Are you sure you want to clear all logs?"
        )

        if result:

            try:
                with open("feds.log", "w") as f:
                    f.write("")

                log_text.delete(1.0, tk.END)
                live_alerts.delete(1.0, tk.END)

                status_label.config(text="📋 Logs cleared successfully")

            except Exception as e:
                status_label.config(text=f"Clear error: {e}")

    def update_live_alerts():

        nonlocal last_read_line

        try:
            with open("feds.log", "r") as f:

                lines = f.readlines()

                new_lines = lines[last_read_line:]

                for line in new_lines:

                    if "[CREATED]" in line:
                        live_alerts.insert(tk.END, line, "created")

                    elif "[MODIFIED]" in line:
                        live_alerts.insert(tk.END, line, "modified")

                    elif "[DELETED]" in line:
                        live_alerts.insert(tk.END, line, "deleted")

                    elif "[MOVED]" in line:
                        live_alerts.insert(tk.END, line, "moved")

                    elif "[RENAMED]" in line:
                        live_alerts.insert(tk.END, line, "renamed")

                    elif "[COPIED]" in line:
                        live_alerts.insert(tk.END, line, "copied")

                    elif "[NETWORK]" in line:
                        live_alerts.insert(tk.END, line, "network")

                    else:
                        live_alerts.insert(tk.END, line)

                    live_alerts.see(tk.END)

                last_read_line = len(lines)

        except FileNotFoundError:
            pass

        global_root.after(1000, update_live_alerts)

    def resize_bg(event):

        nonlocal bg_photo

        if bg_img_original:

            resized = bg_img_original.resize(
                (event.width, event.height),
                Image.Resampling.LANCZOS
            )

            bg_photo = ImageTk.PhotoImage(resized)

            bg_label.config(image=bg_photo)

    def show_event_legend():

        legend_window = tk.Toplevel(global_root)

        legend_window.title("Event Type Legend")
        legend_window.geometry("400x300")
        legend_window.configure(bg="#1e1e1e")

        tk.Label(
            legend_window,
            text="📊 EVENT TYPE LEGEND",
            font=("Helvetica", 14, "bold"),
            fg="white",
            bg="#1e1e1e"
        ).pack(pady=10)

        legend_items = [
            ("📁 [CREATED]", "New file created", "lime"),
            ("📝 [MODIFIED]", "File content/attributes changed", "skyblue"),
            ("🗑 [DELETED]", "File removed", "tomato"),
            ("📦 [MOVED]", "File moved to different directory", "orange"),
            ("✏ [RENAMED]", "File renamed in same directory", "violet"),
            ("📋 [COPIED]", "File copy operation detected", "cyan"),
            ("🌐 [NETWORK]", "Suspicious network activity", "gold")
        ]

        for symbol, description, color in legend_items:

            frame = tk.Frame(legend_window, bg="#1e1e1e")
            frame.pack(fill="x", padx=20, pady=2)

            tk.Label(
                frame,
                text=symbol,
                fg=color,
                bg="#1e1e1e",
                font=("Helvetica", 10, "bold")
            ).pack(side="left")

            tk.Label(
                frame,
                text=description,
                fg="white",
                bg="#1e1e1e",
                font=("Helvetica", 9)
            ).pack(side="left", padx=10)

    try:
        bg_img_original = Image.open("bg.png")

        bg_photo = ImageTk.PhotoImage(bg_img_original)

        bg_label = tk.Label(global_root, image=bg_photo)

        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        global_root.bind("<Configure>", resize_bg)

    except Exception as e:
        print("Background error:", e)

        global_root.configure(bg="#1e1e1e")

    title_frame = tk.Frame(global_root, bg="#1e1e1e")
    title_frame.pack(pady=10)

    tk.Label(
        title_frame,
        text="EXFILGUARD",
        font=("Helvetica", 20, "bold"),
        fg="white",
        bg="#1e1e1e"
    ).pack(side="left", padx=10)

    legend_btn = tk.Button(
        title_frame,
        text="📊 Legend",
        command=show_event_legend,
        bg="#444",
        fg="white",
        font=("Helvetica", 8)
    )

    legend_btn.pack(side="right", padx=10)

    status_label = tk.Label(
        global_root,
        text="🔘 Monitoring Not Running",
        font=("Helvetica", 12),
        fg="white",
        bg="#1e1e1e"
    )

    status_label.pack(pady=5)

    global_root.mainloop()

# ----------------- LOGIN WINDOW -----------------
def start_auth_gui():

    root = tk.Tk()

    root.title("EXFILGUARD Authentication")
    root.geometry("400x350")
    root.configure(bg="#1e1e1e")

    header_frame = tk.Frame(root, bg="#1e1e1e")
    header_frame.pack(pady=20)

    tk.Label(
        header_frame,
        text="🛡",
        font=("Helvetica", 24),
        bg="#1e1e1e",
        fg="white"
    ).pack()

    tk.Label(
        header_frame,
        text="EXFILGUARD",
        font=("Helvetica", 16, "bold"),
        fg="white",
        bg="#1e1e1e"
    ).pack()

    tk.Label(
        header_frame,
        text="File & Network Security Monitor",
        font=("Helvetica", 10),
        fg="#cccccc",
        bg="#1e1e1e"
    ).pack()

    form_frame = tk.Frame(root, bg="#1e1e1e")
    form_frame.pack(pady=20)

    tk.Label(
        form_frame,
        text="Username",
        fg="white",
        bg="#1e1e1e",
        font=("Helvetica", 10)
    ).grid(row=0, column=0, sticky="w", pady=5)

    username_entry = tk.Entry(
        form_frame,
        bg="#2d2d2d",
        fg="white",
        insertbackground="white",
        width=25,
        font=("Helvetica", 10)
    )

    username_entry.grid(row=0, column=1, pady=5, padx=10)

    tk.Label(
        form_frame,
        text="Password",
        fg="white",
        bg="#1e1e1e",
        font=("Helvetica", 10)
    ).grid(row=1, column=0, sticky="w", pady=5)

    password_entry = tk.Entry(
        form_frame,
        show="*",
        bg="#2d2d2d",
        fg="white",
        insertbackground="white",
        width=25,
        font=("Helvetica", 10)
    )

    password_entry.grid(row=1, column=1, pady=5, padx=10)

    def handle_login():
        login(username_entry.get(), password_entry.get(), root)

    tk.Button(
        root,
        text="🔐 Login",
        command=handle_login,
        bg="#1976d2",
        fg="white",
        width=15,
        font=("Helvetica", 10, "bold")
    ).pack(pady=20)

    root.bind("<Return>", lambda event: handle_login())

    root.mainloop()

if __name__ == "__main__":
    start_auth_gui()
