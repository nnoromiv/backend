from sqlalchemy import Column, Integer, String, Float, DateTime
from db import Base

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Integer)
    visibility = Column(Integer)
    condition = Column(String)
    wind_speed = Column(Float)
    timestamp = Column(DateTime)
