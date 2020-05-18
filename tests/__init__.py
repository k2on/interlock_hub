from local_server import *


class LocalServerMock(LocalServer):
    def __init__(self):
        """
        Mock Local Server
        """
        self._is_from_test = True
        super().__init__()
