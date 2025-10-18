from schema.weather import WeatherSchema
from pydantic import ValidationError
from schema.traffic import TrafficSchema
from schema.incident import IncidentSchema
import logging
import datetime
import logging
from psycopg2.extras import execute_values
import json
from db.connection import db_connection
from sqlalchemy import text


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def validate_data(weather, weather_destination, traffic, incidents):
    try:
        w = WeatherSchema(**weather)
    except ValidationError as e:
        logging.error(f"Weather validation failed: {e}")
        w = None
        
    try:
        wD = WeatherSchema(**weather_destination)
    except ValidationError as e:
        logging.error(f"Weather validation failed: {e}")
        wD = None

    try:
        t = TrafficSchema(**traffic)
    except ValidationError as e:
        logging.error(f"Traffic validation failed: {e}")
        t = None

    valid_incidents = []
    for inc in incidents:
        try:
            valid_incidents.append(IncidentSchema(**inc))
        except ValidationError:
            logging.warning(f"Invalid incident skipped: {inc.get('id', 'unknown')}")

    return w, wD, t, valid_incidents

def store_data(weather, weather_destination, traffic, incidents):
    """
    Store Weather, Traffic, TrafficSpeed, and Incidents into PostgreSQL.
    Handles duplicate weather (city) and traffic (origin-destination) by updating timestamp and latest data.
    """
    engine = db_connection()

    try:
        with engine.begin() as conn:
            # ---- WEATHER (Origin) ----
            conn.execute(text("""
                INSERT INTO weather 
                (city, temperature, humidity, visibility, condition, wind_speed, timestamp)
                VALUES (:city, :temperature, :humidity, :visibility, :condition, :wind_speed, :timestamp)
            """),
            vars(weather))
            
            # ---- WEATHER (Destination) ----
            conn.execute(text("""
                INSERT INTO weather (city, temperature, humidity, visibility, condition, wind_speed, timestamp)
                VALUES (:city, :temperature, :humidity, :visibility, :condition, :wind_speed, :timestamp)
            """), vars(weather_destination))

            # ---- TRAFFIC ----
            result = conn.execute(text("""
                INSERT INTO traffic (origin, destination, journey_time_min, journey_time_with_traffic_min,
                                    delay_min, congestion_percentage, timestamp)
                VALUES (:origin, :destination, :journey_time_min, :journey_time_with_traffic_min,
                        :delay_min, :congestion_percentage, :timestamp)
                RETURNING id;
            """), vars(traffic))
            
            traffic_row = result.fetchone()
            traffic_id = traffic_row[0] if traffic_row else None
            
            conn.commit()
                
            # ---- TRAFFIC SPEED ----
            if traffic.traffic_speeds and traffic_id:
                values = [(traffic_id, ts.type, ts.speed_kmh) for ts in traffic.traffic_speeds]

                # execute_values needs a raw connection
                raw_conn = engine.raw_connection()
                try:
                    with raw_conn.cursor() as cur:
                        execute_values(
                            cur,
                            """
                            INSERT INTO traffic_speed (traffic_id, type, speed_kmh)
                            VALUES %s
                            """,
                            values
                        )
                    raw_conn.commit()
                finally:
                    raw_conn.close()

             # ---- INCIDENTS ----
            for inc in incidents:
                conn.execute(text("""
                    INSERT INTO incident (id, severity, category, sub_category, current_update, location,
                                          start_date, end_date, timestamp)
                    VALUES (:id, :severity, :category, :sub_category, :current_update, :location,
                            :start_date, :end_date, :timestamp)
                    ON CONFLICT (id) DO UPDATE
                    SET severity = EXCLUDED.severity,
                        category = EXCLUDED.category,
                        sub_category = EXCLUDED.sub_category,
                        current_update = EXCLUDED.current_update,
                        location = EXCLUDED.location,
                        start_date = EXCLUDED.start_date,
                        end_date = EXCLUDED.end_date,
                        timestamp = EXCLUDED.timestamp;
                """), {
                    "id": inc.id,
                    "severity": inc.severity,
                    "category": inc.category,
                    "sub_category": inc.subCategory,
                    "current_update": inc.currentUpdate,
                    "location": inc.location,
                    "start_date": inc.start_date,
                    "end_date": inc.end_date,
                    "timestamp": inc.timestamp
                })

        logging.info("All data stored successfully in PostgreSQL.")

    except Exception as e:
        logging.error(f"Error storing data: {e}")
        if conn:
            conn.rollback()

    finally:
        if engine:
            engine.dispose()

def export_sample_json():
    engine = db_connection()
    with engine.connect() as conn:
        weather_result = conn.execute(text("SELECT * FROM weather ORDER BY timestamp DESC LIMIT 5;"))
        weather_sample = [dict(row._mapping) for row in weather_result.fetchall()]

        traffic_result = conn.execute(text("SELECT * FROM traffic ORDER BY timestamp DESC LIMIT 5;"))
        traffic_sample = [dict(row._mapping) for row in traffic_result.fetchall()]

        incident_result = conn.execute(text("SELECT * FROM incident ORDER BY timestamp DESC LIMIT 5;"))
        incidents_sample = [dict(row._mapping) for row in incident_result.fetchall()]


        sample = {
            "weather": weather_sample,
            "traffic": traffic_sample,
            "incidents": incidents_sample,
            "source_timestamp": datetime.datetime.now().isoformat()
        }

        with open("sample_traffic_data.json", "w") as f:
            json.dump(sample, f, indent=4, default=str)

        logging.info("Sample JSON exported locally.")

