import time
from .constants import errors
from socketio import Client
from socketio.exceptions import ConnectionError
from .logger import logger


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

    def handle_connection(self):
        """
        Handles a successful connection to the websocket
        :return:
        """
        logger.info("CONNECTION ESTABLISHED")

    def handle_connection_error(self, reason):
        """
        Handles an unsuccessful connection to the websocket
        :param reason: str: reason for the rejection
        :return: None
        """
        logger.error("COULD NOT ESTABLISH WS CONNECTION, REASON: " + reason)

        if reason == errors.INVALID_TOKEN:
            # self.local_server.authenticator.reauthenticate()
            self.disconnect(retry_after=lambda: None)
        elif reason == errors.CONNECTION_REFUSED:
            self.disconnect(retry_after=self.local_server.tester.establish_internet_tests)
        else:
            self.disconnect()
        return False

    def handle_disconnect(self):
        """
        Handles a disconnection from the server
            Depending on the reason, will run the nessisary steps to either reconnect do something else

        :return: None
        """
        logger.error("DISCONNECTED FROM THE WS SERVER")
        self.disconnect()

    def disconnect(self, retry_after=None):
        logger.debug("DISCONNECTING CLIENT")
        self.client.disconnect()
        logger.debug("CLIENT DISCONNECTED")
        if retry_after is None:
            self.retry_connection = False
            logger.error("STOPPING THE PROGRAM")
            return self.local_server.stop()

        if not callable(retry_after):
            raise TypeError("retry_after MUST be a function")

        retry_after()

        logger.info("RETRYING IN 10 SECONDS")
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
            self.client.connect(self.url)
            return True
        except ConnectionError as e:
            self.handle_connection_error((e.args or ["UNKNOWN"])[0])

    def establish_connection(self):
        """
        Will force a connection to the websocket server
        :return: None
        """
        while self.retry_connection:
            ok = self.connect()
            if ok:
                break
            if self.retry_connection:
                logger.debug("RETRYING IN 5 SECONDS")
                time.sleep(5)


