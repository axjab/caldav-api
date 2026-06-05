from os       import getenv
from security import users

class Configurator:
    def __init__(self):
        self.secret_key = load_env("CALDAV_SECRET_KEY", required=True, validator=lambda v: len(v) >= 32)
        self.users_file = load_file("CALDAV_USERS_FILE")
        self.user_database = users # placeholder
        self.a = load_env("AAAAAAAAAAA")
        self.b = load_env("BBBBBBBBBBBBBBBBB")
        self.c = load_env("CCCCCCCCCCCCCCCCCCCCCC")

def load_env(key:str, required=False, validator=None):
    value = getenv(key)
    if required and not value: raise ValueError(f"{key} IS REQUIRED")
    if validator and not validator(value): raise ValueError(f"{key} HAS FAILED VALIDATION")
    print(f"LOADED {key}")
    return value

def load_file(filename:str, required:bool = False, validator = None):
    print(f"NOT IMPLEMENTED. LOCATE {filename}, DOING VALIDATION, ETC ETC.....")
