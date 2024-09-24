import requests
import json
import tkinter as tk
from tkinter import messagebox

# Tomorrow.io API endpoint
tomorrow_url = "https://api.tomorrow.io/v4/timelines"

# Nominatim geocoding API endpoint
nominatim_url = "https://nominatim.openstreetmap.org/search"

# API key
tomorrow_api_key = "7h3V4NhuV091lGgF3kVTXJ282VuwrEmJ"

# Load the weather code mapping from code.json
with open('weather/code.json') as f:
    weather_codes = json.load(f)

def get_coordinates(city_name):
    # Nominatim geocoding API parameters
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }

    # Set the User-Agent header
    headers = {
        "User-Agent": "WeatherApp/1.0"
    }

    # Make GET request to Nominatim API
    response = requests.get(nominatim_url, params=params, headers=headers)

    # Check if the response was successful
    if response.status_code == 200:
        data = json.loads(response.text)
        if data:
            return f"{data[0]['lat']}, {data[0]['lon']}"
        else:
            return None
    else:
        print("Error:", response.status_code)
        return None

def get_weather_data(api_key, location):
    # Tomorrow.io API parameters
    params = {
        "location": location,
        "fields": ["temperature", "temperatureApparent", "humidity", "windSpeed", "windDirection", "cloudCover", "visibility", "pressureSurfaceLevel", "weatherCode"],
        "units": "metric",
        "timesteps": ["current"],
        "apikey": api_key
    }

    # Make GET request to Tomorrow.io API
    response = requests.get(tomorrow_url, params=params)

    # Check if the response was successful
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None

def display_weather_details(weather_data):
    values = weather_data['data']['timelines'][0]['intervals'][0]['values']
    important_details = {
        "Temperature": f"{values['temperature']}°C",
        "Apparent Temperature": f"{values['temperatureApparent']}°C",
        "Humidity": f"{values['humidity']}%",
        "Wind Speed": f"{values['windSpeed']}m/s",
        "Wind Direction": f"{values['windDirection']}°",
        "Cloud Cover": f"{values['cloudCover']}%",
        "Visibility": f"{values['visibility']}m",
        "Pressure": f"{values['pressureSurfaceLevel']}Pa"
    }

    # Get the weather code from the JSON response
    weather_code = values['weatherCode']

    # Get the weather name from the weather code mapping
    weather_name = weather_codes.get(str(weather_code), 'Unknown')

    # Clear the text box
    text_box.delete(1.0, tk.END)

    # Print the weather details
    for key, value in important_details.items():
        text_box.insert(tk.END, f"{key}: {value}\n")

    # Print the weather name
    text_box.insert(tk.END, f"Weather: {weather_name}\n")

def search_weather():
    city_name = city_entry.get()
    coordinates = get_coordinates(city_name)
    if coordinates:
        weather_data = get_weather_data(tomorrow_api_key, coordinates)
        if weather_data:
            display_weather_details(weather_data)
        else:
            messagebox.showerror("Error", "Failed to retrieve weather data")
    else:
        messagebox.showerror("Error", "Failed to retrieve coordinates")

# Create the main window
root = tk.Tk()
root.title("Weather App")

# Set the background color
root.configure(bg="#2ecc71")

# Create the city entry field
city_label = tk.Label(root, text="City:", bg="#2ecc71", fg="#ffffff", font=("Arial", 18))
city_label.grid(row=0, column=0, padx=10, pady=10)
city_entry = tk.Entry(root, width=30, bg="#ecf0f1", fg="#000000", font=("Arial", 18))
city_entry.grid(row=0, column=1, padx=10, pady=10)

# Create the search button
search_button = tk.Button(root, text="Search", command=search_weather, bg="#16a085", fg="#ffffff", font=("Arial", 18))
search_button.grid(row=0, column=2, padx=10, pady=10)

# Create the text box to display the weather details
text_box = tk.Text(root, width=40, height=10, bg="#ecf0f1", fg="#000000", font=("Arial", 18))
text_box.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Add a weather icon
weather_icon = tk.Label(root, text="", bg="#2ecc71", fg="#ffffff")
weather_icon.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
weather_icon.config(text="")
weather_icon.config(font=("Arial", 48))

# Start the main loop
root.mainloop()