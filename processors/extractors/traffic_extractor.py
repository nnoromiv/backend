import os
from dotenv import load_dotenv
import requests
import datetime

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CITY = os.getenv("CITY", "London")
DESTINATION = os.getenv("DESTINATION", "Reading")

if not GOOGLE_API_KEY:
    raise ValueError("Missing API Key. Please set 'GOOGLE_API_KEY' in your .env file.")

def fetch_traffic(origin=CITY, destination=DESTINATION):
    BASE_URL = f"https://maps.googleapis.com/maps/api/directions/json"
    
    # With traffic
    params = {
        "origin": origin,
        "destination": destination,
        "departure_time": "now",
        "mode": "driving",
        "traffic_model": "best_guess",
        "key": GOOGLE_API_KEY
    }
    
    data = requests.get(BASE_URL, params=params).json()
    
    if not data['routes']:
        raise Exception("No route data available")
    
    traffic_leg = data['routes'][0]['legs'][0]
    
    duration = traffic_leg['duration']['value'] / 60 # In Minutes
    duration_in_traffic = traffic_leg['duration_in_traffic']['value'] / 60
    
    delay = duration_in_traffic - duration
    congestion_percentage = (delay / duration) * 100 if duration > 0 else 0
    
    distance_in_km = traffic_leg['distance']['value'] / 1000
    
    speed = distance_in_km / (duration / 60) # In km/h
    speed_in_traffic = distance_in_km / (duration_in_traffic / 60)
    
    delay_clamped = max(round(delay, 2), 0)
    congestion_clamped = max(round(congestion_percentage, 2), 0)
    
    traffic_info = {
        "origin": traffic_leg['start_address'],
        "destination": traffic_leg['end_address'],
        "journey_time_min": round(duration, 2),
        "journey_time_with_traffic_min": round(duration_in_traffic, 2),
        "delay_min": delay_clamped,
        "congestion_percentage": congestion_clamped,
        "traffic_speeds": [
            {
                "type": "no_traffic", 
                "speed_kmh": round(speed, 2)
            },
            {
                "type": "with_traffic", 
                "speed_kmh": round(speed_in_traffic, 2)
            }
        ],
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    return traffic_info
    
if __name__ == "__main__":
    print(fetch_traffic())