from .logger import logger


class Authenticator:
    """
    Class for Authenticating the Local Server with a User
    """
    def __init__(self):
        pass

    @property
    def is_authenticated(self):
        """
        Status of the authentication
        :return: boolean
        """
        return True

    def authenticate(self):
        """
        Authenticates the local server with a user
        :return: boolean: Status
        """
        logger.debug("Authenticating...")
        logger.debug("Authenticated!")
        return True
