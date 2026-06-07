from fastapi    import FastAPI  # type: ignore
from caldav     import aio      # type: ignore
from utils      import Logger
from config     import Configurator
from security   import Authenticator
from services   import CalDAVService
from models     import Event

# TODO:
# 1. Check connection on startup

log  = Logger(name="uvicorn", color="green")  # paramters dont seem to work as intended
conf = Configurator()
auth = Authenticator(conf.api_key)
caldav = CalDAVService(
    url=conf.caldav_url,
    username=conf.username,
    password=conf.password
)

app = FastAPI(title="CalDAV API")

@app.get("/health")
def check_health():
    log("Health check")
    return {"status": "ok", "message": "u good my boi"}

@app.get("/random")
def get_random():
    import random
    return {"random_number": random.randint(1, 100)}

@app.get("/auth", dependencies=[auth()])  # example: dependencies=[auth(), limit(), audit(), log(), etc.]
async def test_auth():
    """Test endpoint to verify API key authentication."""
    log("AUTHORIZED")
    return {"status": "ok", "message": "API key is valid!"}

@app.post("/test-client")  # is it safe without auth?
async def test_davclient():
    """
    Test creating an async DAVClient from explicit config.
    """
    try:
        client = await caldav.get_davclient()
        return {
            "status": "ok",
            "message": "Successfully created DAVClient with provided config.",
            "client_type": type(client).__name__,
            "url": str(client.url)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/calendars")
async def list_calendars():
    result = await caldav.get_calendars()
    return result

@app.get("/calendar/{id}") #TODO auth
async def get_calendar(id:str):
    result = await caldav.get_calendar(id)
    return result

@app.post("/calendar/{name}", dependencies=[auth()])
async def create_calendar(name: str):
    result = await caldav.create_calendar(name)
    log(f"Created new calendar {name}")
    return result

# @app.get("/calendar/{name}/events")                              # GET ALL

# @app.get("/calendars/{calendar_id}/event/{event_id}")            # GET ONE

@app.post("/calendars/{calendar_id}/event")
async def create_event(calendar_id):
    result = await caldav.create_event(calendar_id)
    log(f"{calendar_id}")
    return result

# @app.put("/calendars/{calendar_id}/event/{event_id}")            # UPDATE

# @app.delete("/calendars/{calendar_id}/event/{event_id}")          #DELETE
