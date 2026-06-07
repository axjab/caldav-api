
from fastapi import security, Depends, HTTPException, status  # type: ignore
from secrets import compare_digest


class Authenticator:

    def __init__(self, api_key:str):
        self.header_scheme = security.APIKeyHeader(name="X-API-Key", auto_error=False)
        self.api_key = api_key

    def verify_key(self):
        """Returns a dependency callable. Ref: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/"""
        async def _verify(key: str = Depends(self.header_scheme)):
            if not key or not compare_digest(key, self.api_key):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid API key",
                    headers={"WWW-Authenticate": "API key"}
                )
            return True
        return _verify
