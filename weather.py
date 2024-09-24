import requests
import json
import tkinter as tk
from tkinter import messagebox

def get_weather_gradient(weather_code):
    weather_gradients = {
        "1000": ("#FFD700", "#FF8C00"),  # Clear, Sunny
        "1100": ("#FFE4B5", "#FF8C00"),  # Mostly Clear
        "1101": ("#D3D3D3", "#A9A9A9"),  # Partly Cloudy
        "1102": ("#A9A9A9", "#696969"),  # Mostly Cloudy
        "1001": ("#808080", "#696969"),  # Cloudy
        "2000": ("#C0C0C0", "#A9A9A9"),  # Fog
        "2100": ("#D3D3D3", "#C0C0C0"),  # Light Fog
        "4000": ("#ADD8E6", "#4682B4"),  # Drizzle
        "4001": ("#0000FF", "#00008B"),  # Rain
        "4200": ("#87CEFA", "#4682B4"),  # Light Rain
        "4201": ("#0000CD", "#00008B"),  # Heavy Rain
        "5000": ("#FFFFFF", "#B0C4DE"),  # Snow
        "5001": ("#F0F8FF", "#B0C4DE"),  # Flurries
        "5100": ("#E0FFFF", "#B0E0E6"),  # Light Snow
        "5101": ("#B0E0E6", "#4682B4"),  # Heavy Snow
        "6000": ("#E0FFFF", "#B0C4DE"),  # Freezing Drizzle
        "6001": ("#ADD8E6", "#4682B4"),  # Freezing Rain
        "6200": ("#87CEFA", "#4682B4"),  # Light Freezing Rain
        "6201": ("#0000CD", "#00008B"),  # Heavy Freezing Rain
        "7000": ("#B0C4DE", "#4682B4"),  # Ice Pellets
        "7101": ("#4682B4", "#00008B"),  # Heavy Ice Pellets
        "7102": ("#B0C4DE", "#4682B4"),  # Light Ice Pellets
        "8000": ("#FFA07A", "#FF4500"),  # Thunderstorm
    }

    return weather_gradients.get(weather_code, ("#FFFFFF", "#FFFFFF"))  # default to white if weather code not found

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
    # Get the weather code from the JSON response
    weather_code = weather_data['data']['timelines'][0]['intervals'][0]['values']['weatherCode']

    # Get the gradient colors for the weather code
    gradient_colors = get_weather_gradient(weather_code)

    # Set the background color of the root window to the gradient colors
    root.configure(bg=gradient_colors[0])  # set the background color to the first color in the gradient
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

    # Disable the text box to prevent editing
    text_box.config(state=tk.DISABLED)

def search_weather(event=None):
    city_name = city_entry.get()
    if city_name:
        coordinates = get_coordinates(city_name)
        if coordinates:
            weather_data = get_weather_data(tomorrow_api_key, coordinates)
            if weather_data:
                display_weather_details(weather_data)
                text_box.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
                root.title(f"{city_name} Weather")
                
                # Create and place the credit button
                credit_button = tk.Button(root, text="Credits", command=show_credits)
                credit_button.place(relx=1, rely=1, anchor=tk.SE)
            else:
                messagebox.showerror("Error", "Failed to retrieve weather data")
        else:
            messagebox.showerror("Error", "Failed to retrieve coordinates")
    else:
        messagebox.showerror("Error", "Please enter a city name")

def show_credits():
    # Hide the weather details
    text_box.grid_remove()
    
    # Get current weather gradient
    weather_code = 1000  # Placeholder for demonstration. Replace with the actual weather code if available.
    gradient_colors = get_weather_gradient(str(weather_code))
    
    # Create and place the credit label
    credit_label = tk.Label(root, text="Weather App created by Ashish Joseph", bg=gradient_colors[0], fg="#ffffff", font=("Arial", 18))
    credit_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    
    # Insert the GitHub logo code here
    github_logo = tk.PhotoImage(file="weather/github_logo.png")
    github_label = tk.Label(root, image=github_logo, bg=gradient_colors[0])
    github_label.image = github_logo
    github_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
    
    github_link_label = tk.Label(root, text="GitHub: ", fg="blue", cursor="hand2", bg=gradient_colors[0], font=("Arial", 18))
    github_link_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
    github_link_label.bind("<Button-1>", lambda e: open_github())
    
    # Create and place the back button
    back_button = tk.Button(root, text="Back", command=go_back_to_weather)
    back_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

def go_back_to_weather():
    # Hide the credit label
    for widget in root.grid_slaves():
        widget.grid_remove()
    
    # Show the weather details again
    text_box.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

def open_github():
    import webbrowser
    webbrowser.open("https://github.com/ashishjoseph")

# Create the main window
root = tk.Tk()
root.title("Weather App")

# Set system default background color
root.configure(bg=root.cget("bg"))

# Create a label for the city input
city_label = tk.Label(root, text="Enter a city name:")
city_label.grid(row=0, column=0, padx=10, pady=10)

# Create an entry widget for city input
city_entry = tk.Entry(root)
city_entry.grid(row=0, column=1, padx=10, pady=10)
city_entry.bind("<Return>", search_weather)

# Create a button to trigger the search
search_button = tk.Button(root, text="Search", command=search_weather)
search_button.grid(row=0, column=2, padx=10, pady=10)

# Create a text box to display weather details
text_box = tk.Text(root, width=50, height=15)

# Start the main loop
root.mainloop()
