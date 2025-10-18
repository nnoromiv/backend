-- Incident table
CREATE TABLE IF NOT EXISTS incident (
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
CREATE INDEX IF NOT EXISTS idx_incident_location ON incident(location);
CREATE INDEX IF NOT EXISTS idx_incident_timestamp ON incident(timestamp);
