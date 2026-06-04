from typing import List, Set, Dict, Optional, Literal
from datetime import datetime, time, timedelta
from pydantic import BaseModel, Field
from ipaddress import IPv4Address
from decimal import Decimal
from enum import Enum
from uuid import UUID

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
