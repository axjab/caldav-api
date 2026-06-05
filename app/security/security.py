
import jwt
from fastapi    import security, Depends
from pwdlib     import PasswordHash # type: ignore
from pydantic   import BaseModel    # type: ignore
from typing     import Annotated
from datetime   import datetime, timezone, timedelta
from models     import User

oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class Authenticator:

    def __init__(self,
            user_db,
            secret_key,
            token_timedelta = timedelta(minutes=30),
            signing_algorithm = "HS256",
        ):
        self.password_hash = PasswordHash.recommended()
        self.user_database = user_db
        self.secret_key    = secret_key
        self.algorithm     = signing_algorithm
        self.token_dt      = token_timedelta

    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.get_user(username)
        if not user: return None
        if not self.is_pass_correct(password, user.hash): return None
        return user

    def get_token(self, username: str) -> Token:
        payload = {
            "sub": username,
            "exp": datetime.now(timezone.utc) + self.token_dt
        }
        token = jwt.encode(
            payload,
            self.secret_key,
            self.algorithm
        )
        return Token(access_token=token,token_type="bearer")

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]) -> User | None:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username = payload.get("sub")
            if username is None:
                return None
            user = self.get_user(username)
            return user if user else None
        except jwt.exceptions.InvalidTokenError as e: # need to run uv pip install pyjwt to make this Exception available
            print(e)
            return None
    
    def get_user(self, username: str) -> User | None:
        if username in self.user_database:
            user_dict = self.user_database[username]
            return User(**user_dict)

    def is_pass_correct(self, password, hash) -> bool:
            return self.password_hash.verify(password, hash)
