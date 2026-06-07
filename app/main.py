from fastapi    import FastAPI  # type: ignore
from caldav     import aio      # type: ignore
from utils      import Logger
from config     import Configurator
from security   import Authenticator
from services   import CalDAVService
from models     import Event

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

@app.post("/test-client", dependencies=[auth()])
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

@app.post("/calendar/{name}", dependencies=[auth()])
async def create_calendar(name: str):
    result = await caldav.create_calendar(name)
    log(f"Created new calendar {name}")
    return result

@app.get("/calendars")
async def list_calendars():
    """
    List calendars on a CalDAV server using the provided credentials.
    """
    try:
        async with await aio.get_calendars() as calendars:
            for calendar in calendars:
                print(f"Calendar \"{await calendar.get_display_name()}\" has URL {calendar.url}")
        
        return {
            "status": "ok",
            "message": "Successfully listed calendars. Check server logs for details."
        }

        # client = await aio.get_async_davclient(
        #     url=credentials.url,
        #     username=credentials.username,
        #     password=credentials.password,
        #     features="radicale"
        # )

        # async with client:
        #     principal = await client.get_principal()
        #     calendars = await principal.calendars()

        #     return {
        #         "status": "ok",
        #         "calendars": [
        #             {
        #                 "name": calendar.name,
        #                 "url": str(calendar.url)
        #             }
        #             for calendar in calendars
        #         ]
        #     }

    except Exception as e:
        return {"status": "error", "message": str(e)}
