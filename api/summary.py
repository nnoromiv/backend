from fastapi import APIRouter, HTTPException
from db import db_connection
from processors.processor import generate_full_summary
from fastapi_cache.decorator import cache

summary_router = APIRouter(
    prefix="/api/summary",
    tags=["Summary"]
)

@summary_router.get("/")
@cache(expire=300)
def unified_summary():
    engine = db_connection()
    summary = generate_full_summary(engine)
    return summary

@summary_router.get("/weather-traffic", name="Weather-Traffic Correlation")
@cache(expire=300)
def weather_traffic_correlation():
    try:
        engine = db_connection()
        correlation = generate_full_summary(engine, type="weather_traffic")
        return correlation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
