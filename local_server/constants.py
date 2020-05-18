# Constants for the Local Server
import yaml
from os import path
import logging

# Versions
HUB_VERSION = "1.0"

# Files
CONFIG_PATH = "configuration.yml"
USER_TOKEN_PATH = ".user_token"

ALT_CONFIG_PATHS = ["config.yml", "conf.yml", "settings.yml"]
DEFAULT_CONFIG = {
    "domain": "localhost",
    "machine_id": "WwvsckaAQQLG3Kf3ms41Z0ZJw",
    "confirmation_code": "N38SM4",
    "local_server_port": 8080,
}

if not path.exists(CONFIG_PATH):
    for _alt_path in ALT_CONFIG_PATHS:
        if path.exists(_alt_path):
            CONFIG_PATH = _alt_path
            break

try:
    with open(CONFIG_PATH) as f:
        config = yaml.load(f)
        f.close()
except FileNotFoundError:
    logging.error("NO CONFIG FILE FOUND")
    config = DEFAULT_CONFIG
except Exception as e:
    raise e

# Constants from the config

DOMAIN = config.get("domain", DEFAULT_CONFIG.get("domain"))
MACHINE_ID = config.get("machine_id", DEFAULT_CONFIG.get("machine_id"))
CONFIRMATION_CODE = (
    config.get("confirmation_code", DEFAULT_CONFIG.get("confirmation_code"))
    .upper()
    .strip()
)
if not CONFIRMATION_CODE.isalnum():
    raise ValueError("confirmation code must be alphanumeric")
if len(CONFIRMATION_CODE) != 6:
    raise ValueError("confirmation code must be 6 characters")

MACHINE_SECRET = config.get("machine_secret", None)

if MACHINE_ID == DEFAULT_CONFIG.get("machine_id"):
    raise ValueError("THE MACHINE ID MUST BE CHANGED")
if CONFIRMATION_CODE == DEFAULT_CONFIG.get("confirmation_code"):
    raise ValueError("THE CONFIRMATION CODE MUST BE CHANGED")
if not MACHINE_SECRET:
    raise ValueError("THE MACHINE SECRET MUST BE SET")

LOCAL_SERVER_PORT = config.get(
    "local_server_port", DEFAULT_CONFIG.get("local_server_port")
)

# Internet Constants

LOCAL_DOMAINS = ["localhost", "127.0.0.1"]

IS_LOCAL = DOMAIN in LOCAL_DOMAINS
WS_PROTOCOL = "ws://"
WEB_PROTOCOL = f"http{'s' if not IS_LOCAL else ''}://"  # change to http if your prod server is still using http (why?)
WEB_BASE_URL = f"{WEB_PROTOCOL}{DOMAIN}/"
WS_BASE_URL = f"{WS_PROTOCOL}{DOMAIN}/"
INTERLOCK_URL = f"{WEB_BASE_URL}interlock/"
API_URL = f"{INTERLOCK_URL}api/"
LOCAL_SERVERS_URL = f"{API_URL}local_servers/"

INET_TEST_URI = "https://www.google.com"  # url to test for internet

# Logger constants

LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Error "codes"


class errors:
    CONNECTION_REFUSED = "Connection refused by the server"
    INVALID_TOKEN = "INVALID_TOKEN"


class codes:

    # set up

    INTERNAL_SETUP = 1
    SERVICE_SETUP = 11
    WEBSERVER_SETUP = 111

    RUNNING_TESTS = 12
    RUNNING_INET_TESTS = 121
    RUNNING_INET_TEST = 1211
    RUNNING_SERVER_TEST = 1212

    AUTHORIZING = 13
    NEEDS_USER_AUTH = 131

    ESTABLISHING_WS = 14

    # success

    OK = 2
    TESTS_SUCCESS = 22
    INET_TEST_SUCCESS = 221

    AUTHORIZED = 23

    # 3 class is like a warning

    REAUTHENTICATING = 33
    INVALID_TOKEN_REAUTH = 331

    # errors

    SERVICE_ERROR = 41
    WEBSERVER_SETUP_ERROR = 411

    TEST_ERROR = 42
    INET_TEST_ERROR = 421
    NO_INTERNET = 4211
    NO_SERVER = 4212

    AUTH_FAILED = 43
    GET_TOKEN_REQ_FAILED = 431

    WS_CONNECTION_FAILED = 44

    @classmethod
    def to_name(cls, code):
        for key, item in cls.__dict__.items():
            if type(item) is int and key.isupper() and item == code:
                return key
        return "UNKNOWN"


# Non important but nice things

START_SPLASH_TEXT = """
    _____   __________________  __    ____  ________ __
   /  _/ | / /_  __/ ____/ __ \/ /   / __ \/ ____/ //_/
   / //  |/ / / / / __/ / /_/ / /   / / / / /   / ,<   
 _/ // /|  / / / / /___/ _, _/ /___/ /_/ / /___/ /| |  
/___/_/ |_/ /_/ /_____/_/ |_/_____/\____/\____/_/ |_|  

                created by Max Koon, 2020
"""

END_SPLASH_TEXT = """
                          __   __             
   ____ _____  ____  ____/ /  / /_  __  _____ 
  / __ `/ __ \/ __ \/ __  /  / __ \/ / / / _ \\
 / /_/ / /_/ / /_/ / /_/ /  / /_/ / /_/ /  __/
 \__, /\____/\____/\__,_/  /_.___/\__, /\___/ 
/____/                           /____/       
"""
