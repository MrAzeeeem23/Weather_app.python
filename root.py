#importing all librarys

import tkinter as tk
import requests
import ttkbootstrap
import pytz
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import PhotoImage

current_timezone = None

#Weather Function

#---------------------------------------------API WEATHER---------------------------------------------------------------#
def get_weather(city):

    #API_KEY

    API_key ="01c74fb80536c4fd14598332961183a5"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"

    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error","City is not Founded")
        return None

    if res.status_code == 11001:
        messagebox.showerror("Error","Connect to The Internet")
        return None
    

    #JSON_code</>

    weather = res.json()

    icon_id = weather['weather'][0]['icon']

    temp= weather['main']['temp'] - 273.15

    description = weather['weather'][0]['description']

    city = weather['name']

    country = weather['sys']['country']

    humidity = weather['main']['humidity']

    pressure = weather['main']['pressure']

    wind = weather['wind']['speed']

    timezone = pytz.country_timezones.get(country, ['UTC'])[0]

    global current_timezone
    current_timezone = timezone
    
#icon_url_API_______/

    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"

    return (icon_url, temp,description,city,country,timezone,humidity,pressure,wind)

#--------------------------------------Search_Function-----------------------------------------------------#

def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return

    icon_url, temp, description, city, country, timezone, humidity, pressure, wind = result
    location_label.configure(text=f"{city}, {country}")

    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image) 
    icon_label.configure(image=icon)
    icon_label.image = icon

#main temp.2f is a format

    temp_label.configure(text=f"Temperature: {temp:.0f}°C")
    humidity_label.configure(text=f" Humidity: {humidity}%")
    pressure_label.configure(text=f" Pressure: {pressure}hPa")
    wind_label.configure(text=f" Wind: {wind}m/s")
    description_label.configure(text=f"Description: {description}")   

    current_date_time = datetime.now(pytz.timezone(current_timezone)).strftime("%B %d, %H:%M%p")
    time_label.configure(text=f"Time Zone: {current_timezone}")
    date_time_label.configure(text=f"Date & Time: {current_date_time}")

#Window Box 

root = ttkbootstrap.Window(themename = "morph")
root.title("Weather application.Ak")
root.geometry("600x640")
# root.resizable(False,False) #for fixed window

image_path ="weather_icon.png"
weather_image = PhotoImage(file=image_path)

#----------------Main title heading--------------------#

title = tk.Label(root,font=('Futura-Bold', 25), foreground='#FF0000',compound="left",image=weather_image, text=" Weather App")
title.pack(pady=10)

location_label = tk.Label(root, font=('Helvetica-Bold', 25))
location_label.pack(pady=10)

time_label = tk.Label(root, font="Helvetica, 10")
time_label.pack()

date_time_label = tk.Label(root, font=('Helvetica', 15))
date_time_label.pack()

icon_label = tk.Label(root)
icon_label.pack()

image_path ="tem.png"
temperature_image = PhotoImage(file=image_path)

temp_label = tk.Label(root, font="Helvetica, 20",compound="left", image=temperature_image)
temp_label.pack(pady=20)

weather_info_frame = tk.Frame(root)
weather_info_frame.pack()

image_path ="humidity_icon.png"
humidity_image = PhotoImage(file=image_path)

humidity_label = tk.Label(weather_info_frame, font="Helvetica, 10",compound="left", image=humidity_image)
humidity_label.pack(side=tk.LEFT, padx=5)

image_path ="pressur_icon.png"
pressur_image = PhotoImage(file=image_path)

pressure_label = tk.Label(weather_info_frame, font="Helvetica, 10",compound="left", image=pressur_image)
pressure_label.pack(side=tk.LEFT, padx=5)

image_path ="wind_icon.png"
wind_image = PhotoImage(file=image_path)

wind_label = tk.Label(weather_info_frame, font="Helvetica, 10",compound="left", image=wind_image)
wind_label.pack(side=tk.LEFT, padx=5)


description_label = tk.Label(root, font="Helvetica, 15")
description_label.pack(pady=10)

#---------------------------------placeholder_removal_functions-----------------------------------------#

def on_entry_click(event):
    if city_entry.get() == "Enter City":
        city_entry.delete(0, "end")  
        city_entry.set_style("style", foreground='black')  

def on_focus_out(event):
    if city_entry.get() == "":
        city_entry.insert(0, "Enter City")
        city_entry.set_style("style", foreground='grey') 

#Search_bar

city_entry = ttkbootstrap.Entry(root, font=('helvetica', 18))
city_entry.insert(0, "Enter City")
city_entry.bind("<FocusIn>", on_entry_click)
city_entry.bind("<FocusOut>", on_focus_out)
city_entry.pack(pady=5)

#Set the background color for the "Search" button

style = ttkbootstrap.Style()
style.configure("Custom.TButton", background="#99ebff",padding=(5, 10, 5, 10),)

search_button = ttkbootstrap.Button(root, text="Search",width=30, command=search, style="Custom.TButton", bootstyle="warning")
search_button.pack(pady=20)

author = ttkbootstrap.Label(root, text="By- Azeem Khan", font=('Harlow Solid Italic', 13))
author.pack(padx=10)

root.mainloop()

#Author: "Pathan Azeemkhan Majidkhan"
