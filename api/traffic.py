from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schema.traffic import (
    TrafficResponse,
    TrafficSummaryResponse,
    TrafficHeatmapResponse,
)
from api.services.traffic_service import *
from db import Base, db_connection, get_db
from fastapi_cache.decorator import cache

# Create table if required
Base.metadata.create_all(
    bind = db_connection()
)

traffic_router = APIRouter(prefix="/api/traffic", tags=["Traffic"])

@traffic_router.get("/current", response_model=list[TrafficResponse])
@cache(expire=300)
def traffic_current(db: Session = Depends(get_db)):
    return get_traffic_current(db)


@traffic_router.get("/history", response_model=list[TrafficResponse])
@cache(expire=300)
def traffic_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_traffic_history(db, skip, limit)

@traffic_router.get("/summary", response_model=TrafficSummaryResponse)
@cache(expire=300)
def traffic_summary(db: Session = Depends(get_db)):
    summary = get_traffic_summary(db)
    if not summary:
        raise HTTPException(status_code=404, detail="No traffic data available")
    return summary

@traffic_router.get("/heatmap", response_model=list[TrafficHeatmapResponse])
@cache(expire=300)
def traffic_heatmap(db: Session = Depends(get_db)):
    return get_traffic_heatmap(db)

@traffic_router.post("/refresh")
@cache(expire=300)
def traffic_refresh(db: Session = Depends(get_db)):
    try:
        updated_count = refresh_traffic_data(db)
        return {"status": "success", "message": f"Traffic data refreshed for {updated_count} routes."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@traffic_router.get("/{origin}/{destination}", response_model=TrafficResponse)
@cache(expire=300)
def traffic_route(origin: str, destination: str, db: Session = Depends(get_db)):
    route = get_traffic_route(db, origin, destination)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route
