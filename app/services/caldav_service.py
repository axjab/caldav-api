from utils  import log
from caldav import aio

class CalDAVService:
    """Encapsulates a single CalDAV server session."""

    def __init__(self,
        url: str,
        username: str,
        password: str,
        features: str = "radicale"
        ):
        self.url = url
        self.username = username
        self.password = password
        self.features = features
        self.davclient = None
        self.principal = None
    
    async def get_davclient(self):
        if self.davclient is None:
            self.davclient = await aio.get_async_davclient(
                url=self.url,
                username=self.username,
                password=self.password,
                features=self.features
            )
        return self.davclient
    
    async def get_principal(self):
        if self.principal is None:
            client = self.get_davclient()
            self.principal = await client.get_principal()
        return self.principal
    
    async def create_calendar(self, name:str):
        p = await self.get_principal()
        cal = await p.make_calendar(name)
        return {"name": name}
