from typing import Annotated
from pydantic import BaseModel # type: ignore
from fastapi import Depends, FastAPI, HTTPException # type: ignore
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # type: ignore

app = FastAPI()

# DATA VV

fake_users_db = {
    "johndoe": {
        "name": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret"
    },
    "alice": {
        "name": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2"
    }
}

# DATA ^^

# SECURITY =================================================================v

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    name: str
    email: str | None = None

class UserInDB(User):
    hashed_password: str

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    return user

def decode_token(token):
    return User(
        name=token + ":fakedecoded", email="john@example.com"
    )

def fake_hash_password(password: str):
    return "fakehashed" + password

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.name, "token_type": "bearer"}

# SECURITY =================================================================^

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
