from .logger import logger
from .constants import LOCAL_SERVER_PORT
from werkzeug.serving import make_server
import threading
from flask import Flask


class WebServer:

    class ServerThread(threading.Thread):
        def __init__(self, app):
            threading.Thread.__init__(self)
            self.srv = make_server('0.0.0.0', LOCAL_SERVER_PORT, app)
            self.ctx = app.app_context()
            self.ctx.push()

        def run(self):
            self.srv.serve_forever()

        def stop(self):
            self.srv.shutdown()

    def __init__(self, local_server):
        self.local_server = local_server
        self.app = Flask(__name__)

        @self.app.route('/')
        def index():
            return str(self.local_server.status_code) + " : " + self.local_server.status_code_name

        self.server = self.ServerThread(self.app)

    def start(self):
        logger.debug("STARTING WEBSERVER")
        self.server.start()

    def stop(self):
        logger.info("SHUTTING DOWN THE WEBSERVER...")
        self.server.stop()
        logger.info("SHUT DOWN THE WEBSERVER")

