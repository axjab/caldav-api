from os import getenv
from utils import log

# EXPLANATION:
# THE GATEWAY IS STATELESS IN THE HTTP SENSE:
# NO CLIENT SESSIONS, NO SERVER-SIDE STATE PER REQUEST.
# HOWEVER, IT IS NOT "CONFIGURATIONLESS" — IT IS BOUND AT
# DEPLOYMENT TO A SPECIFIC CALDAV INSTANCE VIA ENVIRONMENT
# CONFIGURATION, NOT CLIENT-SUPPLIED CREDENTIALS.
# THE CLIENT AUTHENTICATES TO THE GATEWAY (API KEY).
# THE GATEWAY AUTHENTICATES TO THE CALDAV SERVER (STORED CREDS).
# THESE ARE TWO SEPARATE SECURITY DOMAINS.


class Configurator:
    def __init__(self):
        self.caldav_url = self.load_env("CALDAV_URL", required=True)
        self.username   = self.load_env("CALDAV_USER", required=True)
        self.password   = self.load_env("CALDAV_PASS", required=True)
        self.api_key    = self.load_env("CALDAV_API_KEY", required=True) # validator=lambda v: len(v) >= 32

    def load_env(self, key:str, required=False, validator=None):
        value = getenv(key)
        if required and not value: raise ValueError(f"{key} IS REQUIRED")
        if validator and not validator(value): raise ValueError(f"{key} HAS FAILED VALIDATION")
        log(f"LOADED {key}")
        return value

    def load_file(self, filename:str, required:bool = False, validator = None):
        log(msg=f"NOT IMPLEMENTED. LOCATE {filename}, DOING VALIDATION, ETC ETC.....")
