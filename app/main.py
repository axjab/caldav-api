from caldav import get_davclient        # type: ignore
from fastapi import FastAPI             # type: ignore
from models import Event


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

@app.get("/davclient")
def read_davclient():
    
    davclient = get_davclient()
    return {"davclient": str(davclient)}
