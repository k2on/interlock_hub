from . import LocalServerMock
import pytest


def test_main():
    local_server = LocalServerMock()
    assert local_server.status_code == 1
    assert local_server.status_code_name == "INTERNAL_SETUP"
