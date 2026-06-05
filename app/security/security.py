import jwt
from pydantic   import BaseModel    # type: ignore
from pwdlib     import PasswordHash # type: ignore
from models     import User

# TODO: Move these to a .env file and load them securely
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class Auth:

    def __init__(self):
        self.password_hash = PasswordHash.recommended()

    def authenticate_user(self, users_data, username: str, password: str):
        user = self.get_user(users_data, username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def verify_password(self, plain_password, hashed_password):
        return self.password_hash.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def get_user(db, username: str):
        if username in db:
            user_dict = db[username]
            return User(**user_dict)
