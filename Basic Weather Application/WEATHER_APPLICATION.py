import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Input error", "Please enter a city name")
        return

    api_key = "89126e7e1314de0389f07c20a4245856"  
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city + "&units=metric"

    response = requests.get(complete_url)
    data = response.json()

    if data.get("cod") != 200:
        messagebox.showerror("Error", data.get("message", "City not found"))
        return

    try:
        weather = data["main"]
        wind = data["wind"]
        description = data["weather"][0]["description"]
        icon_code = data["weather"][0]["icon"]

        temp = weather["temp"]
        pressure = weather["pressure"]
        humidity = weather["humidity"]
        wind_speed = wind["speed"]

        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
        icon_response = requests.get(icon_url)
        icon_image = Image.open(io.BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)

        temp_label.config(text=f"Temperature: {temp}°C")
        pressure_label.config(text=f"Pressure: {pressure} hPa")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_speed_label.config(text=f"Wind Speed: {wind_speed} m/s")
        description_label.config(text=f"Description: {description}")
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

    except KeyError as e:
        messagebox.showerror("Error", f"Unexpected response format: {data}")
        print(data)

app = tk.Tk()
app.title("Weather App")
app.geometry("400x400")

font1 = ('Arial', 14)

tk.Label(app, text="Enter City:", font=font1).pack(pady=10)
city_entry = tk.Entry(app, font=font1)
city_entry.pack(pady=5)

tk.Button(app, text="Get Weather", command=get_weather, font=font1).pack(pady=20)

temp_label = tk.Label(app, text="", font=font1)
temp_label.pack(pady=5)

pressure_label = tk.Label(app, text="", font=font1)
pressure_label.pack(pady=5)

humidity_label = tk.Label(app, text="", font=font1)
humidity_label.pack(pady=5)

wind_speed_label = tk.Label(app, text="", font=font1)
wind_speed_label.pack(pady=5)

description_label = tk.Label(app, text="", font=font1)
description_label.pack(pady=5)

icon_label = tk.Label(app, image=None)
icon_label.pack(pady=5)

app.mainloop()
