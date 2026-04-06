from pydantic import BaseModel, Field
from typing import Optional

class ServerBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    ip_address: str

class ServerCreate(ServerBase):
    pass

class ServerResponse(ServerBase):
    id: int
    status: str
    owner_id: int

    class Config:
        from_attributes = True

class ServerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    ip_address: Optional[str] = None
    status: Optional[str] = None