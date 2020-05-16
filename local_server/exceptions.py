class NoInternetConnection(Exception):
    def __init__(self):
        super().__init__("NO_INTERNET_CONNECTION")


class NoServerConnection(Exception):
    def __init__(self):
        super().__init__("NO_CONNECTION_TO_INTERLOCK_SERVERS")


class RequestFailed(Exception):
    """
    HTTP request that failed
    """
    def __init__(self):
        super().__init__("REQUEST_FAILED")
