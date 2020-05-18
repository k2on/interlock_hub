import logging
from .constants import LOGGER_FORMAT


logger = logging.getLogger("Local Server")
logger.setLevel(logging.DEBUG)

_ch = logging.StreamHandler()
_ch.setLevel(logging.DEBUG)

_formatter = logging.Formatter(LOGGER_FORMAT)
_ch.setFormatter(_formatter)
logger.addHandler(_ch)
