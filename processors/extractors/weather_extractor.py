import os
from dotenv import load_dotenv
import requests
import datetime

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("Missing APi Key. Please set 'API_KEY' in your .env file.")


def fetch_weather(location):
    """
        The function fetches weather information from a specified URL and returns a dictionary containing
        various weather details.
        :return: The `fetch_weather` function returns a dictionary containing information about the weather
        in a specific city. The dictionary includes the city name, temperature, humidity, visibility,
        weather condition, wind speed, and a timestamp of when the weather information was fetched.
    """
    
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}"

    response = requests.get(URL)
    data = response.json()
    
    weather_info = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "visibility": data.get("visibility", None),
        "condition": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    return weather_info

if __name__ == "__main__":
    print(fetch_weather())