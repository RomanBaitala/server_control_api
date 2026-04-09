from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MetricBase(BaseModel):
    server_id: int
    cpu_usage: float = Field(..., ge=0.0, le=100.0)
    cpu_temperature: float = Field(..., ge=0.0, le=150.0)
    memory_usage: float = Field(..., ge=0.0, le=100.0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MetricCreate(MetricBase):
    timestamp: Optional[datetime] = None

class MetricResponse(MetricBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }