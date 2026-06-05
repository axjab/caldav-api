from pydantic import BaseModel, Field   # type: ignore[import]

class CalDAVConfig(BaseModel):
    url: str = Field(..., example="https://caldav.example.com")
    username: str
    password: str
    # ssl_verify_cert: bool = False
    # auth_type: str | None = Field(default=None, examples=["basic", "digest", "bearer"])
    # probe: bool = True
    features: str = "radicale"
