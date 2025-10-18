-- Weather table
CREATE TABLE weather (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100),
    temperature REAL,
    humidity INT,
    visibility INT,
    condition VARCHAR(50),
    wind_speed REAL,
    timestamp TIMESTAMP,
);
CREATE INDEX idx_weather_city ON weather(city);
CREATE INDEX idx_weather_timestamp ON weather(timestamp);

-- Traffic table
CREATE TABLE traffic (
    id SERIAL PRIMARY KEY,
    origin VARCHAR(100),
    destination VARCHAR(100),
    journey_time_min REAL,
    journey_time_with_traffic_min REAL,
    delay_min REAL,
    congestion_percentage REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_traffic_origin_destination_timestamp ON traffic(origin, destination, timestamp);

-- TrafficSpeed table (child of traffic)
CREATE TABLE traffic_speed (
    id SERIAL PRIMARY KEY,
    traffic_id INT REFERENCES traffic(id) ON DELETE CASCADE,
    type VARCHAR(50),
    speed_kmh REAL,
    UNIQUE(traffic_id, type)
);

-- Incident table
CREATE TABLE incident (
    id VARCHAR(100) PRIMARY KEY,
    severity VARCHAR(50),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    current_update TEXT,
    location VARCHAR(200),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    timestamp TIMESTAMP
);
CREATE INDEX idx_incident_location ON incident(location);
CREATE INDEX idx_incident_timestamp ON incident(timestamp);
