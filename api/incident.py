from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from schema.incident import IncidentResponse, IncidentSummaryResponse
from api.services.incident_service import (
    get_incidents_current,
    get_incident_by_id,
    get_active_incidents,
    get_incident_summary,
)
from fastapi_cache.decorator import cache

incident_router = APIRouter(
    prefix="/api/incidents",
    tags=["Incidents"]
)

@incident_router.get("/current", response_model=list[IncidentResponse])
def incidents_current(db: Session = Depends(get_db)):
    return get_incidents_current(db)

@incident_router.get("/active", response_model=list[IncidentResponse])
@cache(expire=300)
def active_incidents(db: Session = Depends(get_db)):
    return get_active_incidents(db)


@incident_router.get("/summary", response_model=IncidentSummaryResponse)
@cache(expire=300)
def incidents_summary(db: Session = Depends(get_db)):
    return get_incident_summary(db)

@incident_router.get("/{id}", response_model=IncidentResponse)
@cache(expire=300)
def incident_by_id(id: str, db: Session = Depends(get_db)):
    incident = get_incident_by_id(db, id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident
