
# deprecated?

from pydantic import BaseModel, Field
from models.user import User    # line 1: ok
# from models import User       # line 2: error

class CalDAVConfig(BaseModel):
    url: str = Field(..., example="https://caldav.example.com")
    user: User
    # ssl_verify_cert: bool = False
    # auth_type: str | None = Field(default=None, examples=["basic", "digest", "bearer"])
    # probe: bool = True
    features: str = "radicale"
