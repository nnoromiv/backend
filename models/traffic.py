from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base


class Traffic(Base):
    __tablename__ = "traffic"

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String, index=True)
    destination = Column(String, index=True)
    journey_time_min = Column(Float)
    journey_time_with_traffic_min = Column(Float)
    delay_min = Column(Float)
    congestion_percentage = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # One-to-many relationship with TrafficSpeed
    traffic_speeds = relationship("TrafficSpeed", back_populates="traffic", cascade="all, delete-orphan")


class TrafficSpeed(Base):
    __tablename__ = "traffic_speed"

    id = Column(Integer, primary_key=True, index=True)
    traffic_id = Column(Integer, ForeignKey("traffic.id"))
    type = Column(String)
    speed_kmh = Column(Float)

    # Link back to parent
    traffic = relationship("Traffic", back_populates="traffic_speeds")
