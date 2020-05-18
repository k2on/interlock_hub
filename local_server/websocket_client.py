import time
from .constants import errors, codes
from socketio import Client
from socketio.exceptions import ConnectionError
from .logger import logger
from .request_handler import RequestHandler


class WebSocketClient:
    """
    WebSocket Client

    This will establish the connection to the Server's WebSocket Server
    Handles errors and stuff

    """

    def __init__(self, ls, url):
        self.local_server = ls
        self.client = Client()
        self.url = url
        self.retry_connection = True
        self.request_handler = RequestHandler(self.local_server)

        @self.client.event
        def connect():
            # Run the handle connection method
            self.handle_connection()

        @self.client.event
        def connect_error(*args):
            # Run the handle connection error method
            reason = (args or ["UNKNOWN"])[0]
            self.handle_connection_error(reason)

        @self.client.event
        def disconnect():
            # Handle disconnection
            self.handle_disconnect()

        @self.client.on("request")
        def request(*args):
            if len(args) == 0:
                logger.error("GOT EMPTY REQUEST")
                return
            self.request_handler.handle(args[0])

    def set_status(self, code):
        return self.local_server.set_status(code)

    def handle_connection(self):
        """
        Handles a successful connection to the websocket
        :return:
        """
        logger.info("CONNECTION ESTABLISHED")
        self.set_status(codes.OK)

    def handle_connection_error(self, reason):
        """
        Handles an unsuccessful connection to the websocket
        :param reason: str: reason for the rejection
        :return: None
        """
        logger.error("COULD NOT ESTABLISH WS CONNECTION, REASON: " + reason)

        if reason == errors.INVALID_TOKEN:
            self.set_status(codes.INVALID_TOKEN_REAUTH)
            self.disconnect(retry_after=self.local_server.authenticator.reauthenticate)
        elif reason == errors.CONNECTION_REFUSED:
            self.disconnect(
                retry_after=self.local_server.tester.establish_internet_tests
            )
        else:
            self.set_status(codes.WS_CONNECTION_FAILED)
            self.disconnect()
        return False

    def handle_disconnect(self):
        """
        Handles a disconnection from the server
            Depending on the reason, will run the nessisary steps to either reconnect do something else

        :return: None
        """
        logger.error("DISCONNECTED FROM THE WS SERVER")

        self.disconnect(retry=True)

    def disconnect(self, retry=False, retry_after=None):
        logger.debug("DISCONNECTING CLIENT")
        self.client.disconnect()
        logger.debug("CLIENT DISCONNECTED")
        if not retry and not callable(retry_after):
            self.retry_connection = False
            logger.error("STOPPING THE PROGRAM")
            return self.local_server.stop()

        if callable(retry_after):
            retry_after()

        logger.info("ESTABLISHING CONNECTION IN 10 SECONDS")
        time.sleep(10)

        return self.establish_connection()

    def connect(self):
        """
        Will establish a connection to the websocket server
            Will handle a connection error and send it to the handle_connection_error method

        :return: Status
        """
        logger.info("ESTABLISHING WEBSOCKET CONNECTION")
        try:
            url = f"{self.url}?token=" + self.local_server.authenticator.token
            self.client.connect(url)
            return True
        except ConnectionError as e:
            self.handle_connection_error((e.args or ["UNKNOWN"])[0])

    def establish_connection(self):
        """
        Will force a connection to the websocket server
        :return: None
        """
        self.set_status(codes.ESTABLISHING_WS)
        while self.retry_connection:
            ok = self.connect()
            if ok:
                break
            if self.retry_connection:
                logger.debug("RETRYING IN 5 SECONDS")
                time.sleep(5)
