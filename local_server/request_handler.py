from local_server import HandlerError
from .logger import logger


class RequestHandler:
    def __init__(self, local_server):
        self.local_server = local_server
        self.ws_client = self.local_server.ws_client

    def handle(self, data):
        try:
            return self.handle_request(data)
        except HandlerError as e:
            logger.error(e.msg)

    def handle_request(self, data):

        handler_map = {
            "MSG": self.handle_message,
            "CMD": None,
            "GET": None
        }

        request_type: str = data.get("t")
        if not request_type:
            raise HandlerError("REQUEST TYPE NOT GIVEN")
        if type(request_type) is not str:
            raise HandlerError("REQUEST TYPE IS NOT STR")
        handler = handler_map.get(request_type.upper())
        if not handler:
            raise HandlerError(request_type + " IS NOT A VALID HANDLER")
        return handler(data)

    def handle_message(self, data):
        message_type = data.get("mt")
        if not message_type:
            raise HandlerError("NO MESSAGE TYPE GIVEN")
        if type(message_type) is not str:
            raise HandlerError("NO MESSAGE TYPE MUST BE STR")
        message_type: str = message_type.upper()

        message = data.get("m")
        if not message:
            raise HandlerError("NO MESSAGE GIVEN")

        if message_type == "DEBUG":
            logger.debug(message)

