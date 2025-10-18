from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WeatherSchema(BaseModel):
    city: str = Field(..., description="Name of the city")
    temperature: float = Field(..., description="Temperature in Kelvin")
    humidity: int = Field(..., description="Humidity percentage")
    visibility: Optional[int] = Field(None, description="Visibility in meters")
    condition: str = Field(..., description="Weather condition, e.g., 'Cloudy'")
    wind_speed: float = Field(..., description="Wind speed in km/h")
    timestamp: datetime = Field(default_factory=datetime.now, description="Data timestamp")
    
class WeatherCreate(WeatherSchema):
    pass

class WeatherResponse(WeatherSchema):
    id: int
    
    model_config = {
        "from_attributes": True
    }
        
class WeatherSummaryResponse(BaseModel):
    avg_temperature: float = Field(..., description="Wind speed in km/h")
    avg_humidity: float = Field(..., description="Wind speed in km/h")
    avg_wind_speed: float = Field(..., description="Wind speed in km/h")
    latest_condition: str = Field(..., description="Wind speed in km/h")
    records_count: int = Field(..., description="Wind speed in km/h")
    
    model_config = {
        "from_attributes": True
    }
