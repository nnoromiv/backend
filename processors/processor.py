import pandas as pd
import numpy as np
import datetime

def generate_full_summary(engine, type: str = "all"):
    """
        Returns a full summary dict of weather, traffic, and incidents.
        Accepts a SQLAlchemy engine.
    """
    summary = {}

    with engine.connect() as conn:
        # ---------------- WEATHER ----------------
        weather_df = pd.read_sql("SELECT * FROM weather;", conn)
        if not weather_df.empty:
            weather_df['timestamp'] = pd.to_datetime(weather_df['timestamp'])
            weather_summary = {
                "avg_temperature": weather_df["temperature"].mean(),
                "avg_humidity": weather_df["humidity"].mean(),
                "avg_wind_speed": weather_df["wind_speed"].mean(),
                "latest_condition": weather_df.sort_values("timestamp").iloc[-1]["condition"],
                "records_count": len(weather_df)
            }
            summary["weather_summary"] = weather_summary

            summary["weather_trend_daily"] = (
                weather_df.groupby(weather_df['timestamp'].dt.date)['temperature']
                .mean()
                .reset_index()
                .to_dict(orient="records")
            )

        # ---------------- TRAFFIC ----------------
        traffic_df = pd.read_sql("SELECT * FROM traffic;", conn)
        if not traffic_df.empty:
            traffic_df['timestamp'] = pd.to_datetime(traffic_df['timestamp'])
            traffic_summary = {
                "avg_delay_min": traffic_df["delay_min"].mean(),
                "avg_congestion_percentage": traffic_df["congestion_percentage"].mean(),
                "avg_journey_time_min": traffic_df["journey_time_min"].mean(),
                "records_count": len(traffic_df)
            }
            summary["traffic_summary"] = traffic_summary

            summary["traffic_trend_daily"] = (
                traffic_df.groupby(traffic_df['timestamp'].dt.date)['congestion_percentage']
                .mean()
                .reset_index()
                .to_dict(orient="records")
            )

        # ---------------- INCIDENTS ----------------
        incident_df = pd.read_sql("SELECT * FROM incident;", conn)
        if not incident_df.empty:
            incident_summary = {
                "total_incidents": len(incident_df),
                "unique_categories": incident_df["category"].nunique(),
                "most_common_category": incident_df["category"].mode().iloc[0],
                "severity_distribution": incident_df["severity"].value_counts().to_dict()
            }
            summary["incident_summary"] = incident_summary

        # ---------------- CORRELATION ----------------
        if not weather_df.empty and not traffic_df.empty:
            merged = traffic_df.assign(key=1).merge(weather_df.assign(key=1), on="key", suffixes=("_traffic", "_weather"))
            merged.drop(columns=["key"], inplace=True)
            corr = merged[["temperature", "humidity", "wind_speed", "delay_min", "congestion_percentage"]].corr()
            corr = corr.replace({np.nan: 0}).round(3)
            summary["weather_traffic_correlation"] = corr.to_dict()

        summary["generated_at"] = datetime.datetime.now().isoformat()        

    return summary if type != "weather_traffic" else summary["weather_traffic_correlation"]