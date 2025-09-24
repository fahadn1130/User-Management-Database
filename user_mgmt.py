import sqlite3
from tabulate import tabulate
import random
import string

#Database setup

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
              CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  username TEXT NOT NULL UNIQUE,
                  department TEXT,
                  email TEXT UNIQUE,   
                  status TEXT DEFAULT 'Active',
                  password TEXT
           )
        """)   
    conn.commit()
    conn.close()

#Helper Functions

def generate_email(username, domain="project.com"):
    return f"{username}@{domain}"

def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))
    
# Core Features

def add_user(name, username, department, email, password):
    # Keep the user-provided email as is
    # Still auto-generate password if not provided
    if not password:  
        password = generate_password()

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (name, username, department, email, password) VALUES (?, ?, ?, ?, ?)",
            (name, username, department, email, password),
        )
        conn.commit()
        print(f"[+] User '{name}' added successfully with email {email}")
    except sqlite3.IntegrityError:
        print("[!] Username or email already exists!")
    conn.close()

    
def list_users():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row  # rows behave like dicts
    c = conn.cursor()
    c.execute("SELECT id, name, username, department, email FROM users")
    rows = c.fetchall()
    conn.close()
    return rows



def delete_user(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def menu():
    while True:
        print("\n-- User Management ---")   
        print("1. Add User")
        print("2. List Users")
        print("3. Exit")

        choice = input("Enter action: ")

        if choice == "1":
            name = input("Enter full name: ")
            username = input("Enter username: ")
            dept = input("Enter department: ")
            add_user(name, username, dept)
        elif choice == '2':
            list_users()
        elif choice == '3':
            break
        else:
            print("Invalid Entry!!")    

if __name__== "__main__":
    init_db()
    menu()
