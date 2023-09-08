from unittest.mock import patch

from pytest import fixture

from crossfire.client import Client


@fixture
def client():
    with patch("crossfire.client.config") as mock:
        mock.side_effect = ("email", "password")
        yield Client()
