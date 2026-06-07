from fastapi    import FastAPI, Depends, HTTPException, status  # type: ignore
from caldav     import aio                  # type: ignore
from typing     import Annotated
from models     import Event
from config     import Configurator
from security   import Authenticator
from services   import CalDAVService

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
    return {"status": "ok", "message": "u good my boi"}

@app.get("/random")
def get_random():
    import random
    return {"random_number": random.randint(1, 100)}

# SECURITY =============================================v

@app.get("/auth", dependencies=[Depends(auth.verify_key())])
async def auth_test():
    """Test endpoint to verify API key authentication."""
    return {"status": "ok", "message": "API key is valid!"}

# SECURITY =============================================^

@app.post("/test-client")
async def test_davclient():
    """
    Test creating an async DAVClient from explicit config.
    """
    try:
        client = await aio.get_async_davclient(**config.model_dump(exclude_none=True))
        
        if client is None:
            return {"status": "error", "message": "Failed to create DAVClient with provided config."}

        my_principal = await client.get_principal()
        return {
            "status": "ok",
            "message": "Successfully created DAVClient with provided config.",
            "client_type": type(client).__name__,
            "url": str(client.url),
            "principal_url": str(my_principal.url) if my_principal else None,
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/calendar/{name}", )
async def create_calendar(name: str):
    """
    ?
    """

    try:
        client = await aio.get_async_davclient(
            url=conf.caldav_url,
            username=conf.username,
            password=conf.password,
            features="radicale"
        )

        async with client:
            principal = await client.get_principal()
            new_calendar = await principal.make_calendar(name=name)

            # TODO: Return canonical Calendar object
            return {
                "status": "created",
                "url": "???",
                "name": calendar_name
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}

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
