
from fastapi import security, Depends, HTTPException, status  # type: ignore
from secrets import compare_digest


class Authenticator:

    def __init__(self, api_key:str):
        self.header_scheme = security.APIKeyHeader(name="X-API-Key", auto_error=False)
        self.api_key = api_key
    
    def __call__(self) -> Depends:
        """Returns the dependency OBJECT (fastapi.Depends)."""
        async def verify_key(key: str = Depends(self.header_scheme)):
            if not key or not compare_digest(key, self.api_key):
                raise HTTPException(status_code=401, detail="Invalid API key")  # This is a CRITICAL line which protects my endpoint. Without it, access is granted REGARDLESS of return value.
            return True  # this return value is meaningless in this context
        
        return Depends(verify_key)
