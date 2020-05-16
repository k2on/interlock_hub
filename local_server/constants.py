# Constants for the Local Server
import yaml
from os import path
import logging

# Files
CONFIG_PATH = "configuration.yml"
ALT_CONFIG_PATHS = [
    "config.yml",
    "conf.yml",
    "settings.yml"
]
DEFAULT_CONFIG = {
    "domain": "localhost"
}

if not path.exists(CONFIG_PATH):
    for _alt_path in ALT_CONFIG_PATHS:
        if path.exists(_alt_path):
            CONFIG_PATH = _alt_path
            break

try:
    with open(CONFIG_PATH) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        f.close()
except FileNotFoundError:
    logging.error("NO CONFIG FILE FOUND")
    config = DEFAULT_CONFIG
except Exception as e:
    raise e

# Constants from the config

DOMAIN = config.get('domain', DEFAULT_CONFIG.get('domain'))

# Internet Constants

LOCAL_DOMAINS = ["localhost", "127.0.0.1"]

IS_LOCAL = DOMAIN in LOCAL_DOMAINS
WS_PROTOCOL = "ws://"
WEB_PROTOCOL = f"http{'s' if not IS_LOCAL else ''}://"  # change to http if your prod server is still using http (why?)
WEB_BASE_URL = f"{WEB_PROTOCOL}{DOMAIN}/"
WS_BASE_URL = f"{WS_PROTOCOL}{DOMAIN}/"
API_URL = f"{WEB_PROTOCOL}api/"

INET_TEST_URI = "https://www.google.com"  # url to test for internet

# Logger constants

LOGGER_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class errors:
    CONNECTION_REFUSED = "Connection refused by the server"
    INVALID_TOKEN = "INVALID_TOKEN"
