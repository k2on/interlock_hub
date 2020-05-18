from .logger import logger
import time
import requests
import platform
from .exceptions import RequestFailed
from .constants import (
    MACHINE_ID,
    MACHINE_SECRET,
    LOCAL_SERVERS_URL,
    HUB_VERSION,
    USER_TOKEN_PATH,
    codes,
)
from os import path


class Authenticator:
    """
    Class for Authenticating the Local Server with a User
    """

    def __init__(self, local_server):
        self.local_server = local_server
        self.token = self.get_saved_token()

    def set_status(self, code):
        return self.local_server.set_status(code)

    @staticmethod
    def get_saved_token():
        if not path.exists(USER_TOKEN_PATH):
            return None
        with open(USER_TOKEN_PATH) as f:
            token = f.read()
            if token.lower() in ["invalid", ""]:
                return None
            f.close()
            return token

    @property
    def is_authenticated(self):
        """
        Status of the authentication
        :return: boolean
        """
        return self.token is not None

    def reauthenticate(self):
        self.set_status(codes.REAUTHENTICATING)
        self.save_token("invalid")
        return self.authenticate()

    def authenticate(self):
        """
        Authenticates the local server with a user
        :return: boolean: Status
        """
        logger.debug("Authenticating...")

        token = self.establish_user_link()
        self.save_token(token)

        logger.debug("Authenticated!")
        return True

    def save_token(self, token):
        with open(USER_TOKEN_PATH, "w") as f:
            f.write(token)
            f.close()
            self.token = token
        return True

    def establish_user_link(self):
        """
        Establishes a link with a user
        :return: user token
        """
        logger.debug("ESTABLISHING USER LINK")
        token = None
        while not token:
            token = self.get_user_token()
            if token:
                break
            time.sleep(5)
        logger.debug("USER LINK ESTABLISHED")
        self.set_status(codes.AUTHORIZED)
        return token

    def get_user_token(self):
        try:
            url = f"{LOCAL_SERVERS_URL}{MACHINE_ID}"
            machine_data = platform.uname()
            response = requests.get(
                url,
                params={
                    "os": machine_data.system,
                    "machine_name": machine_data.node,
                    "os_version": machine_data.version,
                    "hub_version": HUB_VERSION,
                    "secret": MACHINE_SECRET,
                },
            )
            # TODO: add error handling

            if not response.ok:
                raise RequestFailed(response)

            return response.json().get("user_token")

        except requests.ConnectionError:
            logger.error("USER LINK REQUEST FAILED, TESTING INTERNET CONNECTION")
            self.local_server.tester.establish_internet_tests()
            return self.get_user_token()
        except RequestFailed as rf:
            if "msg" in rf.resp.json():
                reason = rf.resp.json().get("msg")
            else:
                reason = rf.resp.reason
            logger.fatal("USER LINK REQUEST FAILED, REASON: " + str(reason))
            self.set_status(codes.GET_TOKEN_REQ_FAILED)
            exit()
