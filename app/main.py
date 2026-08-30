from pykit.config   import Configurator, env # ignore
from pykit.logging  import Logger
from pykit.security import Authenticator
from fastapi    import FastAPI  # type: ignore
from caldav     import aio      # type: ignore
from services   import CalDAVService
from models     import Event

# TODO:
# 1. Check connection on startup

# DEPENDENCIES ========================================

# HOST: MUST PROVIDE CRITICAL VALUES
conf = Configurator(
    caldav_url=env("CALDAV_URL", required=True),
    username=env("CALDAV_USER", required=True),
    password=env("CALDAV_PASS", required=True),
    api_key=env("CALDAV_API_KEY", required=True, validator=lambda v: len(v) >= 32),
    timeout=env("TIMEOUT", default=30),
    literal_value=42,  # non-env values pass through
    logger_name="uvicorn",
    logger_color="green"
)

# LOG: NEED TO SEE WHAT'S GOING ON
log  = Logger(name="uvicorn", color="green")  # paramters dont seem to work as intended

# AUTH: MUST BLOCK ANONYMOUS USERS
auth = Authenticator(conf.api_key)

caldav = CalDAVService(
    url=conf.caldav_url,
    username=conf.username,
    password=conf.password
)

# SERVICE 2: example
# service2=...

# CODE DOES NOT PROCEED UNLESS UNLESS THESE ARE SORTED FIRST

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
