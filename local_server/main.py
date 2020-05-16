from .authenticator import Authenticator
from .websocket_client import WebSocketClient
from .constants import API_URL, WEB_BASE_URL, WS_BASE_URL
from .exceptions import NoInternetConnection, NoServerConnection
from .tester import Tester

from .logger import logger


class LocalServer:
    """
    Main class for the local server
    """
    def __init__(self):
        # WebSocket client
        self.ws_client = WebSocketClient(self, WS_BASE_URL)
        # User authentication
        self.authenticator = Authenticator()
        # Runs tests for the system
        self.tester = Tester()

    def run(self):
        """
        Method for starting the system
            Runs all the tests
            Authenticates with a user
            Establishes Websocket connection

        :return: Nothing
        """
        logger.info("Starting Local Server")

        # tests system
        self.tester.establish_successful_tests()

        # work on the authenticator
        if not self.authenticator.is_authenticated:
            self.authenticator.authenticate()

        self.ws_client.establish_connection()

    def stop(self, code=None):
        """
        Stops the system

        :param code: Code or reason for the shut down
        :return: None
        """
        logger.info("SHUTTING DOWN...")
        logger.debug("good bye <3")
        # exit(code)

