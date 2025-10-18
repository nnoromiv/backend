from db import Base, db_connection, get_db
from fastapi import APIRouter, Depends, HTTPException
from schema.weather import WeatherResponse, WeatherSummaryResponse
from sqlalchemy.orm import Session
from api.services.weather_service import *
import pandas as pd
from fastapi_cache.decorator import cache

# Create table if required
Base.metadata.create_all(
    bind = db_connection()
)

weather_router = APIRouter(
    prefix="/api/weather",
    tags=['Weather']
)

@weather_router.get("/current", response_model=list[WeatherResponse])
@cache(expire=300)
def weather_current(db:Session = Depends(get_db)):
    return get_weather_current(db)

@weather_router.get("/history", response_model=list[WeatherResponse])
@cache(expire=300)
def weather_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_weather_history(db, skip, limit)

@weather_router.get("/summary", response_model=WeatherSummaryResponse)
@cache(expire=300)
def weather_summary(db: Session = Depends(get_db)):
    weather = get_weather_current(db)
    
    if not weather:
        return WeatherSummaryResponse(
            avg_temperature=0.0,
            avg_humidity=0.0,
            avg_wind_speed=0.0,
            latest_condition="N/A",
            records_count=0
        )
        
    weather_list = [
        {
            "temperature": w.temperature,
            "humidity": w.humidity,
            "wind_speed": w.wind_speed,
            "condition": w.condition,
            "timestamp": w.timestamp
        } for w in weather
    ]
        
    df = pd.DataFrame(weather_list)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return WeatherSummaryResponse(
        avg_temperature=df["temperature"].mean(),
        avg_humidity=df["humidity"].mean(),
        avg_wind_speed=df["wind_speed"].mean(),
        latest_condition=df.sort_values("timestamp").iloc[-1]["condition"],
        records_count=len(df)
    )
    
@weather_router.post("/refresh")
@cache(expire=300)
def weather_refresh(db: Session = Depends(get_db)):
    """
    Refreshes weather data for all cities stored in the database.
    It fetches latest weather for each city and updates the record.
    """
    try:
        updated_count = refresh_weather_data(db)
        return {
            "status": "success",
            "message": f"Weather data refreshed for {updated_count} cities."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@weather_router.get("/cities", response_model=list[str])
def weather_cities(db: Session = Depends(get_db)):
    """
    Return all unique city names from the latest weather records.
    """
    return get_weather_cities(db)   


@weather_router.get("/{city}", response_model=WeatherResponse)
@cache(expire=300)
def weather_city(city: str, db: Session = Depends(get_db)):
    weather = get_weather_by_city(db, city)
    if not weather:
        raise HTTPException(status_code=404, detail="City not found")
    
    return weather
