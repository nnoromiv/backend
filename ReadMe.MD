# **UTIS Traffic & Weather API**

## **Overview**

This FastAPI backend serves traffic, weather, and incident data collected from APIs and stored in PostgreSQL. It provides processed trends, summaries, correlations, and visual data for integration with dashboards or other clients.

---

## **API Endpoints**

### **Weather**

| Endpoint               | Method | Description                                 |
| ---------------------- | ------ | ------------------------------------------- |
| `/api/weather/current` | GET    | Latest weather for all cities               |
| `/api/weather/{city}`  | GET    | Latest weather for a specific city          |
| `/api/weather/history` | GET    | Historical weather (paginated)              |
| `/api/weather/summary` | GET    | Weather summary: averages, latest condition |
| `/api/weather/refresh` | POST   | Fetch new weather data from OpenWeatherMap  |

### **Traffic**

| Endpoint                              | Method | Description                         |
| ------------------------------------- | ------ | ----------------------------------- |
| `/api/traffic/current`                | GET    | Latest traffic for all routes       |
| `/api/traffic/{origin}/{destination}` | GET    | Traffic for a specific route        |
| `/api/traffic/history`                | GET    | Historical traffic data (paginated) |
| `/api/traffic/summary`                | GET    | Traffic summary: averages, counts   |
| `/api/traffic/refresh`                | POST   | Fetch new traffic data from TfL API |

### **Incidents**

| Endpoint                 | Method | Description                                 |
| ------------------------ | ------ | ------------------------------------------- |
| `/api/incidents/current` | GET    | Active incidents                            |
| `/api/incidents/{id}`    | GET    | Detailed info for an incident               |
| `/api/incidents/summary` | GET    | Aggregated counts and severity distribution |

### **Summary & Correlation**

| Endpoint                       | Method | Description                                 |
| ------------------------------ | ------ | ------------------------------------------- |
| `/api/summary`                 | GET    | Combined weather, traffic, incident summary |
| `/api/summary/weather-traffic` | GET    | Weather–traffic correlation matrix          |
| `/api/summary/overview`        | GET    | Top-level indicators: counts, averages      |

### **Visualizations**

| Endpoint                          | Description                     | Returns                         |
| --------------------------------- | ------------------------------- | ------------------------------- |
| `/api/visuals/congestion-gauge`   | Overall congestion level        | `{ overall_congestion: 14.31 }` |
| `/api/visuals/congestion-heatmap` | Origin-destination congestion % | GeoJSON / list                  |
| `/api/visuals/traffic-trend`      | Time-series congestion/delay    | Line chart data                 |
| `/api/visuals/weather-trend`      | Temperature/humidity trend      | Line chart data                 |
| `/api/visuals/weather-impact`     | Weather ↔ traffic correlations  | Heatmap / scatter data          |

### **System & Data**

| Endpoint             | Description                       | Returns       |
| -------------------- | --------------------------------- | ------------- |
| `/api/data/sample`   | Latest 5 records from all tables  | JSON sample   |
| `/api/data/export`   | Full dataset export               | Download JSON |
| `/api/system/health` | DB connection + freshness check   | Status info   |
| `/api/system/stats`  | Record counts & latest timestamps | Admin metrics |

---

## **Quick Start**

1. Set PostgreSQL environment variables:

```bash
    POSTGRES_HOST, 
    POSTGRES_PORT, 
    POSTGRES_DB, 
    POSTGRES_USER, 
    POSTGRES_PASSWORD
    API_KEY  # OpenWeatherMap
```

Install dependencies:

```bash
    pip install -r requirements.txt
```

Run FastAPI:

```bash
    fastapi dev main.py
```

Visit **Swagger UI** for interactive API docs:

```bash
    http://127.0.0.1:8000/docs
```

Ensure `entrypoint.sh` is executable

```bash
chmod +x backend/entrypoint.sh
```

---

## **Features**

* ✅ Upsert storage with `ON CONFLICT` to prevent duplicates
* ✅ Trends, averages, and correlations for weather & traffic
* ✅ Historical and current data retrieval with pagination
* ✅ Optional visual endpoints for dashboards
* ✅ Sample JSON and full dataset export

---

## **Notes**

* Anti-bot scraping (Google Maps/Waze) was unreliable; Direction APIs are used.
* Weather ↔ traffic correlation is precomputed for fast response.
* FastAPI cache is recommended for expensive endpoints (e.g., `/summary`).
