from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TrafficSpeed(BaseModel):
    type: str = Field(..., description="Type of road segment or speed measurement")
    speed_kmh: float = Field(..., description="Speed in kilometers per hour")
    
    model_config = {
        "from_attributes": True
    }


class TrafficSchema(BaseModel):
    origin: str = Field(..., description="Starting point of the journey")
    destination: str = Field(..., description="Destination point of the journey")
    journey_time_min: float = Field(..., description="Normal journey time in minutes")
    journey_time_with_traffic_min: float = Field(..., description="Journey time with traffic in minutes")
    delay_min: float = Field(..., description="Delay in minutes due to traffic")
    congestion_percentage: float = Field(..., description="Traffic congestion percentage")
    traffic_speeds: Optional[List[TrafficSpeed]] = Field(..., description="List of speed data for segments")
    timestamp: datetime = Field(default_factory=datetime.now, description="Data timestamp")
    
class TrafficCreate(TrafficSchema):
    pass

class TrafficResponse(TrafficSchema):
    id: int
    
    model_config = {
        "from_attributes": True
    }
    
class TrafficSummaryResponse(BaseModel):
    avg_delay_min: float
    avg_congestion_percentage: float
    avg_journey_time_min: float
    total_origin: int
    total_destination: int

    model_config = {"from_attributes": True}

class TrafficHeatmapResponse(BaseModel):
    origin: str
    destination: str
    congestion_percentage: float

    model_config = {"from_attributes": True}
