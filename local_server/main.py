from .authenticator import Authenticator
from .websocket_client import WebSocketClient
from .constants import API_URL, WEB_BASE_URL, WS_BASE_URL, START_SPLASH_TEXT, END_SPLASH_TEXT, codes
from .tester import Tester
from .web_server import WebServer
from .logger import logger


class LocalServer:
    """
    Main class for the local server
    """
    def __init__(self):
        self.status_code = codes.INTERNAL_SETUP
        # WebSocket client
        self.ws_client = WebSocketClient(self, WS_BASE_URL)
        # WebServer
        self.web_server = WebServer(self)
        # User authentication
        self.authenticator = Authenticator(self)
        # Runs tests for the system
        self.tester = Tester(self)

    @property
    def status_code_name(self):
        return codes.to_name(self.status_code)

    def run(self):
        """
        Method for starting the system
            Runs all the tests
            Authenticates with a user
            Establishes Websocket connection

        :return: Nothing
        """
        print(START_SPLASH_TEXT)
        logger.info("Starting Local Server")

        # Start the Web Server
        try:
            self.set_status(codes.WEBSERVER_SETUP)
            self.web_server.start()
        except:
            logger.error("COULD NOT START THE WEBSERVER")
            self.set_status(codes.WEBSERVER_SETUP_ERROR)

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
        self.web_server.stop()
        logger.debug("good bye <3")
        print(END_SPLASH_TEXT)
        # exit(code)

    def set_status(self, code):
        """
        Sets the internal status code
        :param code: int of the status code
        :return: None
        """
        self.status_code = code
