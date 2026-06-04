from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from uuid import UUID
from enum import Enum
from typing import List, Dict, Set, Optional, Literal, Union
from ipaddress import IPv4Address

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Metadata(BaseModel):
    created: datetime
    version: int = 1

class Event(BaseModel):
    # Primitives
    id: UUID
    summary: str
    description: Optional[str] = None
    is_all_day: bool = False
    
    # Numbers
    sequence: int = Field(ge=0)
    duration: float = Field(gt=0)
    cost: Decimal = Decimal("0.00")
    
    # Temporal
    start: datetime
    end: datetime
    reminder: Optional[time] = None
    offset: timedelta
    
    # Collections
    attendees: List[str] = []
    categories: Set[str] = set()
    properties: Dict[str, str] = {}
    
    # Special
    status: Status = Status.ACTIVE
    visibility: Literal["public", "private"] = "private"
    server_ip: IPv4Address
    
    # Nested
    metadata: Metadata

app = FastAPI()

@app.post("/events")
async def create(event: Event):
    return event

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/health")
def check_health():
    return "u good my boi"
