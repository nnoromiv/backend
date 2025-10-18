from sqlalchemy import Column, String, DateTime
from datetime import datetime
from db import Base


class Incident(Base):
    __tablename__ = "incident"

    id = Column(String, primary_key=True, index=True)
    severity = Column(String)
    category = Column(String)
    sub_category = Column(String)
    current_update = Column(String)
    location = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    timestamp = Column(DateTime, default=datetime.utcnow)
