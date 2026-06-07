
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
        self.client = None
        self.principal = None