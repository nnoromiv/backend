from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
import pandas as pd
import json
from db import get_db

system_router = APIRouter(
    prefix="/api",
    tags=["System"]
)


@system_router.get("/data/sample")
def latest_samples(db: Session = Depends(get_db)):
    """
    Returns the latest 5 samples from weather, traffic, and incidents.
    """
    try:
        sample = {}

        weather_df = pd.read_sql("SELECT * FROM weather ORDER BY timestamp DESC LIMIT 5;", db.bind)
        traffic_df = pd.read_sql("SELECT * FROM traffic ORDER BY timestamp DESC LIMIT 5;", db.bind)
        incident_df = pd.read_sql("SELECT * FROM incident ORDER BY timestamp DESC LIMIT 5;", db.bind)

        sample["weather"] = weather_df.to_dict(orient="records")
        sample["traffic"] = traffic_df.to_dict(orient="records")
        sample["incidents"] = incident_df.to_dict(orient="records")

        return sample
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@system_router.get("/data/export")
def export_full_dataset(db: Session = Depends(get_db)):
    """
    Exports full dataset for weather, traffic, and incidents.
    Returns JSON.
    """
    try:
        full_data = {}

        weather_df = pd.read_sql("SELECT * FROM weather;", db.bind)
        traffic_df = pd.read_sql("SELECT * FROM traffic;", db.bind)
        incident_df = pd.read_sql("SELECT * FROM incident;", db.bind)

        full_data["weather"] = weather_df.to_dict(orient="records")
        full_data["traffic"] = traffic_df.to_dict(orient="records")
        full_data["incidents"] = incident_df.to_dict(orient="records")

        return full_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@system_router.get("/system/health")
def system_health(db: Session = Depends(get_db)):
    """
    Checks DB connectivity and latest timestamps for data freshness.
    """
    try:
        health_info = {}

        # Check DB connection by a simple query
        db.execute(text('SELECT 1'))

        # Latest timestamps
        weather_ts = pd.read_sql("SELECT MAX(timestamp) AS ts FROM weather;", db.bind).iloc[0]["ts"]
        traffic_ts = pd.read_sql("SELECT MAX(timestamp) AS ts FROM traffic;", db.bind).iloc[0]["ts"]
        incident_ts = pd.read_sql("SELECT MAX(timestamp) AS ts FROM incident;", db.bind).iloc[0]["ts"]

        health_info["status"] = "ok"
        health_info["latest_timestamps"] = {
            "weather": str(weather_ts),
            "traffic": str(traffic_ts),
            "incidents": str(incident_ts)
        }

        return health_info
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@system_router.get("/system/stats")
def system_stats(db: Session = Depends(get_db)):
    """
    Returns record counts and latest timestamps for admin dashboard.
    """
    try:
        stats = {}

        weather_stats = pd.read_sql("SELECT COUNT(*) AS count, MAX(timestamp) AS latest FROM weather;", db.bind).iloc[0]
        traffic_stats = pd.read_sql("SELECT COUNT(*) AS count, MAX(timestamp) AS latest FROM traffic;", db.bind).iloc[0]
        incident_stats = pd.read_sql("SELECT COUNT(*) AS count, MAX(timestamp) AS latest FROM incident;", db.bind).iloc[0]

        stats["weather"] = {"records": int(weather_stats["count"]), "latest_timestamp": str(weather_stats["latest"])}
        stats["traffic"] = {"records": int(traffic_stats["count"]), "latest_timestamp": str(traffic_stats["latest"])}
        stats["incidents"] = {"records": int(incident_stats["count"]), "latest_timestamp": str(incident_stats["latest"])}

        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
