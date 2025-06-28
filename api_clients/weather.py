import requests
import os

API_KEY = "be85745c0bdf5f37fc99296e4c626564"

def get_weather(city=None):
    if city:
        location = city
    else:
        try:
            ip_data = requests.get("https://ipinfo.io/json").json()
            location = ip_data.get("city")
        except:
            location = "chettippadi"  # fallback default

    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        return f"Weather in {location}: {temp}°C, {desc}"
    else:
        return "Could not fetch weather data."