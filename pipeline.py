import os
import logging
from utils import validate_data, store_data, export_sample_json
from processors.extractors.weather_extractor import fetch_weather
from processors.extractors.traffic_extractor import fetch_traffic
from processors.extractors.incident_extractor import fetch_incidents

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def run_pipeline():
    ORIGIN = os.getenv("ORIGIN", "London")
    DESTINATION = os.getenv("DESTINATION", "Reading")

    weather_result = fetch_weather(ORIGIN)
    weather_destination_result = fetch_weather(DESTINATION)

    traffic_result = fetch_traffic(ORIGIN, DESTINATION)
    incidents_result = fetch_incidents()

    weather, weather_destination, traffic, incidents = validate_data(weather_result, weather_destination_result, traffic_result, incidents_result)

    if not weather or not weather_destination or not traffic:
        raise ValueError("Validation failed for critical data components (weather or traffic).")
    
    if weather and weather_destination and traffic and incidents is not None:
        store_data(weather, weather_destination, traffic, incidents)
    else:
        logging.warning("No valid data to store. Skipping database insert.")

    export_sample_json()


if __name__ == "__main__":
    run_pipeline()
