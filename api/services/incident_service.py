from sqlalchemy.orm import Session
from models.incident import Incident
from datetime import datetime
import pandas as pd


def get_incidents_current(db: Session):
    return db.query(Incident).order_by(Incident.timestamp.desc()).all()


def get_incident_by_id(db: Session, id: str):
    return db.query(Incident).filter(Incident.id == id).first()


def get_active_incidents(db: Session):
    now = datetime.now()
    return (
        db.query(Incident)
        .filter(Incident.end_date > now)
        .order_by(Incident.start_date)
        .all()
    )


def get_incident_summary(db: Session):
    incidents = db.query(Incident).all()
    if not incidents:
        return {
            "total_incidents": 0,
            "unique_categories": 0,
            "most_common_category": "N/A",
            "severity_distribution": {}
        }

    df = pd.DataFrame([i.__dict__ for i in incidents])

    severity_counts = df["severity"].value_counts().to_dict()
    most_common_category = df["category"].mode().iloc[0] if not df["category"].empty else "N/A"

    return {
        "total_incidents": len(df),
        "unique_categories": df["category"].nunique(),
        "most_common_category": most_common_category,
        "severity_distribution": severity_counts
    }
