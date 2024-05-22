import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        bmi = weight / (height * height)
        bmi = round(bmi, 2)

        
        user_name = user_entry.get()
        if user_name == "":
            messagebox.showerror("Input error", "Please enter your name")
            return

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO bmi_data (user_name, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)",
                       (user_name, weight, height, bmi, date))
        conn.commit()

        result_label.config(text=f'BMI: {bmi:.2f}')
        messagebox.showinfo("BMI Result", f'Your BMI is {bmi:.2f}')

    except ValueError:
        messagebox.showerror("Input error", "Please enter valid numbers for weight and height")

def view_history():
    user_name = user_entry.get()
    if user_name == "":
        messagebox.showerror("Input error", "Please enter your name to view history")
        return

    cursor.execute("SELECT date, bmi FROM bmi_data WHERE user_name = ?", (user_name,))
    records = cursor.fetchall()
    
    if not records:
        messagebox.showinfo("No Data", "No historical data found for this user")
        return

    dates = [record[0] for record in records]
    bmis = [record[1] for record in records]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, bmis, marker='o')
    plt.xlabel('Date')
    plt.ylabel('BMI')
    plt.title(f'BMI Trend for {user_name}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


conn = sqlite3.connect('bmi_data.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS bmi_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    date TEXT
)
''')
conn.commit()


app = tk.Tk()
app.title('BMI Calculator')
app.geometry('600x400')
app.config(bg="#000")

font1 = ('Arial', 20, 'bold')
font2 = ('Arial', 15, 'bold')

tk.Label(app, text='BMI Calculator', font=font1, bg="#000", fg="#fff").pack(pady=10)

tk.Label(app, text='Name', font=font2, bg="#000", fg="#fff").pack(pady=5)
user_entry = tk.Entry(app, font=font2)
user_entry.pack(pady=5)

tk.Label(app, text='Weight (kg)', font=font2, bg="#000", fg="#fff").pack(pady=5)
weight_entry = tk.Entry(app, font=font2)
weight_entry.pack(pady=5)

tk.Label(app, text='Height (m)', font=font2, bg="#000", fg="#fff").pack(pady=5)
height_entry = tk.Entry(app, font=font2)
height_entry.pack(pady=5)

tk.Button(app, text='Calculate BMI', font=font2, command=calculate_bmi).pack(pady=10)
tk.Button(app, text='View History', font=font2, command=view_history).pack(pady=10)

result_label = tk.Label(app, text='', font=font2, bg="#000", fg="#fff")
result_label.pack(pady=20)

app.mainloop()

conn.close()
