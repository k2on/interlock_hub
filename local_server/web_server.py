from .logger import logger
from .constants import LOCAL_SERVER_PORT
from werkzeug.serving import make_server
import threading
from flask import Flask


class WebServer:
    class ServerThread(threading.Thread):
        def __init__(self, app, is_from_test=False):
            threading.Thread.__init__(self)
            try:
                self.srv = make_server("0.0.0.0", LOCAL_SERVER_PORT, app)
            except OSError as e:
                if not is_from_test:
                    raise e
            self.ctx = app.app_context()
            self.ctx.push()

        def run(self):
            self.srv.serve_forever()

        def stop(self):
            self.srv.shutdown()

    def __init__(self, local_server):
        self.local_server = local_server
        self.app = Flask(__name__)

        @self.app.route("/")
        def index():
            return (
                str(self.local_server.status_code)
                + " : "
                + self.local_server.status_code_name
            )

        self.server = self.ServerThread(self.app, self.local_server._is_from_test)

    def start(self):
        """
        Starts the webserver
        :return: None
        """
        logger.debug("STARTING WEBSERVER")
        self.server.start()

    def stop(self):
        """
        Stops the webserver
        :return: None
        """
        logger.info("SHUTTING DOWN THE WEBSERVER...")
        self.server.stop()
        logger.info("SHUT DOWN THE WEBSERVER")
