import tkinter as tk
from tkinter import messagebox
import user_mgmt
from user_mgmt import add_user, delete_user, list_users

def refresh_user_list():
    user_list.delete(0, tk.END)
    users = user_mgmt.list_users()
    for u in users:
        user_list.insert(
            tk.END,
            f"{u['id']}: {u['username']} ({u['email']}) - {u['department']} dept"
        )

def add_user_gui():
    popup = tk.Toplevel(root)
    popup.title("Add User")

    tk.Label(popup, text="Name").grid(row=0, column=0, padx=5, pady=2, sticky="e")
    name_entry = tk.Entry(popup)
    name_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(popup, text="Username").grid(row=1, column=0, padx=5, pady=2, sticky="e")
    username_entry = tk.Entry(popup)
    username_entry.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(popup, text="Department").grid(row=2, column=0, padx=5, pady=2, sticky="e")
    dept_entry = tk.Entry(popup)
    dept_entry.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(popup, text="Email").grid(row=3, column=0, padx=5, pady=2, sticky="e")
    email_entry = tk.Entry(popup)
    email_entry.grid(row=3, column=1, padx=5, pady=2)

    tk.Label(popup, text="Password").grid(row=4, column=0, padx=5, pady=2, sticky="e")
    password_entry = tk.Entry(popup, show="*")
    password_entry.grid(row=4, column=1, padx=5, pady=2)

    def save_user():
        name = name_entry.get().strip()
        username = username_entry.get().strip()
        dept = dept_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not (name and username and dept and email and password):
            messagebox.showerror("Error", "All fields are required!")
            return

        user_mgmt.add_user(name, username, dept, email, password)
        popup.destroy()
        refresh_user_list()
        messagebox.showinfo("Success", "User added successfully!")

    tk.Button(popup, text="Save", command=save_user).grid(
        row=5, columnspan=2, pady=10
    )

def delete_user_gui():
    selection = user_list.curselection()
    if not selection:
        return
    user_text = user_list.get(selection[0])
    user_id = int(user_text.split(":")[0])  # extract ID
    user_mgmt.delete_user(user_id)
    refresh_user_list()

# --- Main Window ---
root = tk.Tk()
root.title("User Management System")
root.geometry("500x350")

frame = tk.Frame(root)
frame.pack(pady=10)

user_list = tk.Listbox(frame, width=60, height=12)
user_list.pack()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

add_btn = tk.Button(btn_frame, text="Add User", command=add_user_gui)
add_btn.grid(row=0, column=0, padx=5)

del_btn = tk.Button(btn_frame, text="Delete User", command=delete_user_gui)
del_btn.grid(row=0, column=1, padx=5)

refresh_btn = tk.Button(btn_frame, text="Refresh", command=refresh_user_list)
refresh_btn.grid(row=0, column=2, padx=5)

refresh_user_list()  # populate on start
root.mainloop()
