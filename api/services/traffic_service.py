from sqlalchemy.orm import Session
from models.traffic import Traffic
from datetime import datetime
import pandas as pd
from sqlalchemy import func, and_


def get_traffic_current(db: Session):
    # Get the latest timestamp for each origin-destination pair
    subquery = (
        db.query(
            Traffic.origin,
            Traffic.destination,
            func.max(Traffic.timestamp).label("latest_timestamp")
        )
        .group_by(Traffic.origin, Traffic.destination)
        .subquery()
    )

    # Join back to get full row data for only the latest records
    latest_records = (
        db.query(Traffic)
        .join(
            subquery,
            and_(
                Traffic.origin == subquery.c.origin,
                Traffic.destination == subquery.c.destination,
                Traffic.timestamp == subquery.c.latest_timestamp,
            ),
        )
        .all()
    )

    return latest_records

def get_traffic_route(db: Session, origin: str, destination: str):
    return (
        db.query(Traffic)
        .filter(
            Traffic.origin.ilike(f"%{origin}%"),
            Traffic.destination.ilike(f"%{destination}%")
        )
        .order_by(Traffic.timestamp.desc())
        .first()
    )

def get_traffic_history(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(Traffic)
        .order_by(Traffic.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_traffic_summary(db: Session):
    df = pd.read_sql(db.query(Traffic).statement, db.bind)
    if df.empty:
        return None
    return {
        "avg_delay_min": df["delay_min"].mean(),
        "avg_congestion_percentage": df["congestion_percentage"].mean(),
        "avg_journey_time_min": df["journey_time_min"].mean(),
        "total_origin": len(df),
        "total_destination": df["destination"].nunique(),
    }

def get_traffic_heatmap(db: Session):
    df = pd.read_sql(db.query(Traffic).statement, db.bind)
    if df.empty:
        return []
    heatmap = df[["origin", "destination", "congestion_percentage"]]
    return heatmap.to_dict(orient="records")

def refresh_traffic_data(db: Session):
    """
    Simulate a refresh.
    """
    routes = db.query(Traffic.origin, Traffic.destination).distinct().all()
    if not routes:
        raise Exception("No routes found in database to refresh.")

    updated_count = 0
    for (origin, destination) in routes:
        # Simulated values (in production, fetch from API)
        congestion = 40 + updated_count * 2
        delay = 5 + updated_count
        avg_speed = 60 - updated_count * 0.5
        incidents = updated_count % 3

        record = (
            db.query(Traffic)
            .filter(Traffic.origin == origin, Traffic.destination == destination)
            .first()
        )
        if record:
            record.congestion_percent = congestion
            record.avg_speed = avg_speed
            record.delay_minutes = delay
            record.incidents = incidents
            record.timestamp = datetime.utcnow()
        else:
            db.add(
                Traffic(
                    origin=origin,
                    destination=destination,
                    congestion_percent=congestion,
                    avg_speed=avg_speed,
                    delay_minutes=delay,
                    incidents=incidents,
                    timestamp=datetime.utcnow(),
                )
            )

        updated_count += 1

    db.commit()
    return updated_count
