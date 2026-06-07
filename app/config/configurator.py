import os, logging

# Use Uvicorn's logger to match its format exactly
logger = logging.getLogger("uvicorn")
MAGENTA = "\033[35m"
RESET = "\033[0m"

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
        self.caldav_url = load_env("CALDAV_URL", required=True)
        self.username   = load_env("CALDAV_USER", required=True)
        self.password   = load_env("CALDAV_PASS", required=True)
        self.api_key    = load_env("CALDAV_API_KEY", required=True) # validator=lambda v: len(v) >= 32

def load_env(key:str, required=False, validator=None):
    value = os.getenv(key)
    if required and not value: raise ValueError(f"{key} IS REQUIRED")
    if validator and not validator(value): raise ValueError(f"{key} HAS FAILED VALIDATION")
    logger.info(f"{MAGENTA}LOADED {key}{RESET}")
    return value

def load_file(filename:str, required:bool = False, validator = None):
    logger.info(f"{MAGENTA}NOT IMPLEMENTED. LOCATE {filename}, DOING VALIDATION, ETC ETC.....{RESET}")
