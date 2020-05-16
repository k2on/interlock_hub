import time

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

        @self.client.event
        def connect():
            # Run the handle connection method
            self.handle_connection()

        @self.client.event
        def connect_error(*args):
            # Run the handle connection error method
            self.handle_connection_error((args or ["UNKNOWN"])[0])

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
        return False

    def handle_disconnect(self):
        """
        Handles a disconnection from the server
            Depending on the reason, will run the nessisary steps to either reconnect do something else

        :return: None
        """
        logger.error("DISCONNECTED FROM THE WS SERVER")
        self.client.disconnect()
        logger.error("STOPPING THE PROGRAM")
        self.local_server.stop()

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
        while True:
            ok = self.connect()
            if ok:
                break
            logger.debug("RETRYING IN 5 SECONDS")
            time.sleep(5)


