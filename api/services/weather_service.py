from sqlalchemy.orm import Session
from models.weather import Weather
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from sqlalchemy import func, and_

load_dotenv()

API_KEY = os.getenv("API_KEY", "")

if not API_KEY:
    raise ValueError("Missing APi Key. Please set 'API_KEY' in your .env file.")

def get_weather_current(db: Session):
        # Get the latest timestamp for each origin-destination pair
    subquery = (
        db.query(
            Weather.city,
            func.max(Weather.timestamp).label("latest_timestamp")
        )
        .group_by(Weather.city)
        .subquery()
    )

    # Join back to get full row data for only the latest records
    latest_records = (
        db.query(Weather)
        .join(
            subquery,
            and_(
                Weather.city == subquery.c.city,
                Weather.timestamp == subquery.c.latest_timestamp,
            ),
        )
        .all()
    )

    return latest_records


def get_weather_cities(db: Session):
    """
    Fetch all unique city names from the latest weather records.
    """
    # Step 1: Get latest timestamp per city
    subquery = (
        db.query(
            Weather.city,
            func.max(Weather.timestamp).label("latest_timestamp")
        )
        .group_by(Weather.city)
        .subquery()
    )

    # Step 2: Join back to get distinct cities (you could also just use subquery directly)
    cities = (
        db.query(subquery.c.city)
        .all()
    )

    # Return as a simple list of strings
    return [city[0] for city in cities]


def get_weather_by_city(db: Session, city:str):
    return db.query(Weather).filter(Weather.city.ilike(city)).order_by(Weather.timestamp.desc()).first()

def get_weather_history(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Weather).order_by(Weather.timestamp.desc()).offset(skip).limit(limit).all()

def refresh_weather_data(db: Session):
    """
    Goes through all unique cities in the DB, calls OpenWeather API for each,
    then updates their weather data (temperature, humidity, etc.).
    """
    cities = db.query(Weather.city).distinct().all()
    if not cities:
        raise Exception("No cities found in database to refresh.")

    updated_count = 0
    URL_TEMPLATE = "http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    for (city_name,) in cities:
        url = URL_TEMPLATE.format(city=city_name, api_key=API_KEY)
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch data for {city_name}: {response.status_code}")
            continue

        data = response.json()

        # Extract relevant fields safely
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        visibility = data.get("visibility", 0)

        # Find existing city record
        existing = db.query(Weather).filter(Weather.city == city_name).first()

        if existing:
            # Update existing record
            existing.temperature = temperature
            existing.humidity = humidity
            existing.condition = condition
            existing.wind_speed = wind_speed
            existing.visibility = visibility
            existing.timestamp = datetime.utcnow()
        else:
            # Create new record if not exists
            new_entry = Weather(
                city=city_name,
                temperature=temperature,
                humidity=humidity,
                condition=condition,
                wind_speed=wind_speed,
                visibility=visibility,
                timestamp=datetime.utcnow()
            )
            db.add(new_entry)

        updated_count += 1

    db.commit()
    return updated_count

