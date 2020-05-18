from requests import get, ConnectionError
from .constants import INET_TEST_URI, WEB_BASE_URL, codes
from .exceptions import NoInternetConnection, NoServerConnection
from .logger import logger

import time


class Tester:
    """
    Tests the system's capabilities
        Will not allow the system to run without critical systems to be operational
    """

    def __init__(self, local_server):
        self.local_server = local_server

    @staticmethod
    def establish_network_connection(func):
        """
        Makes sure a function returns True, will go into a loop till it is reached

        This is used to check network connections

        :param func: Function that should return True
        :return: boolean, should only be True
        """
        ok = func()
        if ok:
            return True
        while not ok:
            ok = func()
            if ok:
                break
            logger.debug("TRYING AGAIN IN 5 SECONDS")
            time.sleep(5)
        return True

    @classmethod
    def establish_network_connections(cls, *funcs):
        """
        Runs the establish_network_connection from an array of functions

        :param funcs: list of functions to return True
        :return: boolean, should only be True
        """
        for func in funcs:
            cls.establish_network_connection(func)
        return True

    def set_status(self, code):
        return self.local_server.set_status(code)

    def establish_successful_tests(self):
        """
        Runs the system's tests
            Will only return if all critical systems to be operational

        :return: boolean, should only be True
        """
        # TODO: when adding this to ras pi, add tests for lights or screens or whatever
        logger.info("ESTABLISHING SYSTEM TESTS")
        self.set_status(codes.RUNNING_TESTS)
        self.establish_internet_tests()
        self.set_status(codes.TESTS_SUCCESS)
        logger.info("ALL TESTS SUCCEEDED")
        return True

    def test_network_connection(self, url, connection_type, error_code):
        """
        Will test the connection to a given URL

        :param url: str: URL to connect to
        :param connection_type: str: used for debug
        :return: boolean, status of the connection
        """

        def func():
            logger.debug(f"TESTING {connection_type} CONNECTION")
            try:
                get(url)
                logger.debug(f"{connection_type} CONNECTION ESTABLISHED")
                return True
            except ConnectionError:
                logger.error(f"NO {connection_type} CONNECTION")
                self.set_status(error_code)
                return False

        return func

    def establish_internet_tests(self):
        """
        Tests the connection to internet services

        :return: boolean, should only be True
        """
        logger.info("ESTABLISHING INTERNET TESTS")
        self.set_status(codes.RUNNING_INET_TEST)
        self.establish_network_connections(
            self.test_network_connection(INET_TEST_URI, "INTERNET", codes.NO_INTERNET),
            self.test_network_connection(WEB_BASE_URL, "SERVER", codes.NO_SERVER),
        )
        logger.info("ALL INTERNET TESTS SUCCEEDED")
        self.set_status(codes.INET_TEST_SUCCESS)
        return True
