import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    try:
        length = int(length_entry.get())
        
        if length <= 0:
            raise ValueError("Length must be positive")

        char_sets = ""
        if var_uppercase.get():
            char_sets += string.ascii_uppercase
        if var_lowercase.get():
            char_sets += string.ascii_lowercase
        if var_digits.get():
            char_sets += string.digits
        if var_special.get():
            char_sets += string.punctuation

        if char_sets == "":
            messagebox.showerror("Input error", "Please select at least one character set")
            return

        password = ''.join(random.choice(char_sets) for _ in range(length))

        password_entry.config(state=tk.NORMAL)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
        password_entry.config(state=tk.READONLY)
    except ValueError as e:
        messagebox.showerror("Input error", str(e))

def copy_to_clipboard():
    password = password_entry.get()
    if password:
        app.clipboard_clear()
        app.clipboard_append(password)
        messagebox.showinfo("Clipboard", "Password copied to clipboard")
    else:
        messagebox.showerror("Clipboard error", "No password to copy")

app = tk.Tk()
app.title("Advanced Password Generator")
app.geometry("400x400")

font1 = ('Arial', 14)

tk.Label(app, text="Password Length:", font=font1).pack(pady=5)
length_entry = tk.Entry(app, font=font1)
length_entry.pack(pady=5)

var_uppercase = tk.BooleanVar()
tk.Checkbutton(app, text="Include Uppercase Letters", variable=var_uppercase, font=font1).pack(pady=5)

var_lowercase = tk.BooleanVar()
tk.Checkbutton(app, text="Include Lowercase Letters", variable=var_lowercase, font=font1).pack(pady=5)

var_digits = tk.BooleanVar()
tk.Checkbutton(app, text="Include Digits", variable=var_digits, font=font1).pack(pady=5)

var_special = tk.BooleanVar()
tk.Checkbutton(app, text="Include Special Characters", variable=var_special, font=font1).pack(pady=5)

tk.Button(app, text="Generate Password", command=generate_password, font=font1).pack(pady=10)

password_entry = tk.Entry(app, font=font1, state="readonly")
password_entry.pack(pady=5)

tk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard, font=font1).pack(pady=5)

app.mainloop()


