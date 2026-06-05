from datetime import timedelta

from fastapi    import FastAPI, Depends, HTTPException, status  # type: ignore
from fastapi.security import OAuth2PasswordRequestForm # type: ignore
from caldav     import aio                  # type: ignore
from typing     import Annotated
from models     import CalDAVConfig, Event
from security   import Auth, Token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, users

app = FastAPI()
auth = Auth()

@app.get("/health")
def check_health():
    return {"status": "ok", "message": "u good my boi"}

@app.get("/random")
def get_random():
    # geenrate random object
    import random
    return {"random_number": random.randint(1, 100)}

# SECURITY =============================================v
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = auth.authenticate_user(users_data=users, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
# SECURITY =============================================^

@app.post("/test-client")
async def test_davclient(config: CalDAVConfig):
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

@app.post("/calendar/{name}")
async def create_calendar(
    credentials:CalDAVConfig,
    name: str
):
    """
    Create a calendar on a CalDAV server using the provided credentials and calendar name.
    """
    try:
        # TODO: USE FASTAPI SECURITY, DO NOT TAKE CREDENTIALS IN THE BODY LIKE THIS
        client = await aio.get_async_davclient(
            url=credentials.url,
            username=credentials.username,
            password=credentials.password,
            features="radicale"
        )

        async with client:
            principal = await client.get_principal()
            new_calendar = await principal.make_calendar(name=name)

            # TODO: Return canonical Calendar object
            return {
                "status": "created",
                "url": "???",
                "name": name
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/calendars")
async def list_calendars(credentials: CalDAVConfig):
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
