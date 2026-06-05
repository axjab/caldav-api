from fastapi    import FastAPI, Depends, HTTPException, security, status  # type: ignore
from caldav     import aio                  # type: ignore
from typing     import Annotated
from models     import CalDAVConfig, User
from config     import Configurator
from security   import Authenticator, Token

conf = Configurator(
    # USE THE FOLLOWING FOR TESTING:
    # CALDAV_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
    # USER=ahmad
    # PASS=test
)
auth = Authenticator( # should I pass key-pairs or the entire conf instead?
    user_db=conf.user_database,
    secret_key=conf.secret_key
)
app = FastAPI()

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
async def login(
    form_data: Annotated[security.OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth.get_token(user.name)

@app.get("/users/me/")
async def read_users_me(
    current_user: Annotated[User, Depends(auth.get_current_user)],
) -> User:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return current_user
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
