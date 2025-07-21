import tkinter as tk
from tkinter import messagebox
import secrets
import string
import os

PASSWORD_FILE = 'last_password.txt'
PASSWORD_HISTORY_FILE = 'password_history.txt'

# === Core Logic ===
def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def save_password(password):
    with open(PASSWORD_FILE, 'w') as file:
        file.write(password)
    with open(PASSWORD_HISTORY_FILE, 'a') as history:
        history.write(password + '\n')

def get_last_password(length):
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as file:
            content = file.read().strip()
            if content == '':
                # If file is empty, generate and save a new one
                new_password = generate_password(length)
                save_password(new_password)
                return new_password
            return content
    else:
        # If file doesn't exist, generate and save a new one
        new_password = generate_password(length)
        save_password(new_password)
        return new_password

# === GUI Setup ===
def on_generate():
    try:
        length = int(length_entry.get())
        if length <= 4:
            raise ValueError
        password = generate_password(length)
        save_password(password)
        output_label.config(text=f"✅ Generated: {password}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a number greater than 4.")

def on_show_last():
    try:
        length = int(length_entry.get())
        if length <= 4:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a number greater than 4.")
        return

    last = get_last_password(length)
    output_label.config(text=f"📂 Last: {last}")

root = tk.Tk()
root.title("🔐 Password Manager")
root.geometry("400x250")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

# === Widgets ===
title = tk.Label(root, text="Password Manager", font=("Helvetica", 16, "bold"), fg="white", bg="#1e1e1e")
title.pack(pady=10)

length_label = tk.Label(root, text="Password Length:", fg="white", bg="#1e1e1e")
length_label.pack()

length_entry = tk.Entry(root, width=10, font=("Helvetica", 12))
length_entry.pack(pady=5)
length_entry.insert(0, "12")

generate_btn = tk.Button(root, text="Generate Password", command=on_generate, bg="#007acc", fg="white", font=("Helvetica", 12), padx=10)
generate_btn.pack(pady=5)

show_btn = tk.Button(root, text="Show Last Password", command=on_show_last, bg="#444", fg="white", font=("Helvetica", 12), padx=10)
show_btn.pack(pady=5)

output_label = tk.Label(root, text="", wraplength=350, fg="lightgreen", bg="#1e1e1e", font=("Courier", 10))
output_label.pack(pady=15)

root.mainloop()
