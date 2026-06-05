from pydantic import BaseModel

# REFERENCE: https://fastapi.tiangolo.com/tutorial/security/get-current-user/

class User(BaseModel):
    name: str
    email: str | None = None
