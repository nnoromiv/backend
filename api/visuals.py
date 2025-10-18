from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd

from db import get_db, db_connection
from processors.processor import generate_full_summary

visuals_router = APIRouter(
    prefix="/api/visuals",
    tags=["Visuals"]
)

@visuals_router.get("/congestion-gauge")
def congestion_gauge():
    """
    Returns overall congestion percentage (average across all traffic records).
    """
    try:
        engine = db_connection()
        summary = generate_full_summary(engine)
        overall_congestion = summary.get("traffic_summary", {}).get("avg_congestion_percentage", 0.0)
        return {"overall_congestion": round(overall_congestion, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@visuals_router.get("/weather-trend")
def weather_trend(db: Session = Depends(get_db)):
    """
    Returns daily temperature/humidity trend.
    """
    try:
        engine = db_connection()
        summary = generate_full_summary(engine)
        trend = summary.get("weather_trend_daily", [])

        # Include humidity in same trend if available
        weather_df = pd.read_sql("SELECT timestamp, humidity FROM weather;", db.bind)
        if not weather_df.empty:
            weather_df['timestamp'] = pd.to_datetime(weather_df['timestamp'])
            humidity_trend = (
                weather_df.groupby(weather_df['timestamp'].dt.date)['humidity']
                .mean()
                .reset_index()
                .to_dict(orient="records")
            )
            for i, record in enumerate(trend):
                if i < len(humidity_trend):
                    record["humidity"] = humidity_trend[i]["humidity"]

        return trend
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    