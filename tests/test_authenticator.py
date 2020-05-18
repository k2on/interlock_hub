# Test the Authenticator
import pytest
from . import LocalServerMock


def test_authenticator():
    local_server = LocalServerMock()
    assert local_server.authenticator is not None
    authenticator = local_server.authenticator
