from datetime import datetime, timedelta
from decimal import Decimal

from models import Status
from fastapi import FastAPI             # type: ignore
from models import Event
from typing import List, Set, Dict, Optional, Literal
from datetime import datetime, time, timedelta
from pydantic import BaseModel, Field
from ipaddress import IPv4Address
from decimal import Decimal
from enum import Enum
from uuid import UUID


app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/health")
def check_health():
    return {"status": "ok", "message": "u good my boi"}

@app.get("/random")
def get_random():
    # geenrate random object
    import random
    return {"random_number": random.randint(1, 100)}

@app.post("/events")
async def create(event: Event):
    return event

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/events/{is_all_day}/{status}/{cost}/{start}/{end}/{offset}/{visibility}/{server_ip}/{uuid}")
def read_event(
    is_all_day: bool,
    status: Status,
    cost: Decimal,
    start: datetime,
    end: datetime,
    offset: timedelta,
    visibility: Literal["public", "private"],
    server_ip: IPv4Address,
    uuid: UUID
):
    return {
        "is_all_day": is_all_day,
        "status": status,
        "cost": cost,
        "start": start,
        "end": end,
        "offset": offset,
        "attendees": attendees,
        "categories": categories,
        "properties": properties,
        "visibility": visibility,
        "server_ip": server_ip,
        "uuid": uuid
    }
