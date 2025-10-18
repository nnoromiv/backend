from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict

class IncidentSchema(BaseModel):
    id: str = Field(..., description="Incident Id")
    severity: str = Field(..., description="Severity level of the incident")
    category: str = Field(..., description="Category of the incident")
    sub_category: str = Field(..., description="Sub-category of the incident")
    current_update: str = Field(..., description="Latest update or status")
    location: str = Field(..., description="Location of the incident")
    start_date: datetime = Field(..., description="Start time of the incident")
    end_date: datetime = Field(..., description="Expected or actual end time of the incident")
    timestamp: datetime = Field(default_factory=datetime.now, description="Data timestamp")
    
class IncidentCreate(IncidentSchema):
    pass

class IncidentResponse(IncidentSchema):
    id: str
    
    model_config = {
        "from_attributes": True
    }
    
class IncidentSummaryResponse(BaseModel):
    total_incidents: int
    unique_categories: int
    most_common_category: str
    severity_distribution: Dict[str, int]
    
