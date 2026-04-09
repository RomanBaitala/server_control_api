from pydantic import BaseModel, Field, field_serializer
from typing import Optional
from datetime import datetime, timezone

class MetricBase(BaseModel):
    server_id: int
    cpu_usage: float = Field(..., ge=0.0, le=100.0)
    cpu_temperature: float = Field(..., ge=0.0, le=150.0)
    memory_usage: float = Field(..., ge=0.0, le=100.0)
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))

class MetricCreate(MetricBase):
    timestamp: Optional[datetime] = None

class MetricResponse(MetricBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

    @field_serializer('timestamp')
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat()