
from caldav import aio
from utils  import log
from datetime import datetime, timezone

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
        log(f"Connected to {self.url}")
        return self.davclient
    
    async def get_principal(self):
        if self.principal is None:
            client = await self.get_davclient()
            self.principal = await client.get_principal()
        return self.principal
    
    async def get_calendars(self):
        p = await self.get_principal()
        calendars = await p.calendars()
        return {
            "calendars": [
                {
                    "name": await cal.name,
                    "url": cal.url.url_raw
                }
                for cal in calendars
            ]
        }
    
    async def get_calendar(self, id:str):
        c = await self.get_davclient()
        # p = await self.get_principal()
        cal = await c.get_calendars()
        log(dir(cal))
        return {"x":"FUCK"}
    
    async def create_calendar(self, name:str):
        p = await self.get_principal()
        cal = await p.make_calendar(name)
        return {"name": name, "detail": f"Created new calendar called {name}"}

    # ..... READ here

    async def create_event(self, calendar_id):
        p = await self.get_principal()
        calendars = await p.calendars()
        cal = calendars[7]   # TODO: turn in to calendar object
        log(cal.name)
        e = await cal.add_event(
            uid="zzzzzzzzzzzz",
            dtstamp=datetime.now(timezone.utc),
            dtstart=datetime(2026,6,7,8),
            dtend=datetime(2026,6,7,10),
            summary="check fastmail",
            rrule={'FREQ': 'YEARLY'})
        prop = e.icalendar_component  # turn into event object
        return {"x":prop}
