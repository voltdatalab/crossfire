from unittest.mock import patch

from pytest import fixture

from crossfire.client import Client, Token


DEFAULT_TOKEN_EXPIRES_IN = 3600


@fixture
def client():
    with patch("crossfire.client.config") as mock:
        mock.side_effect = ("email", "password")
        yield Client()


@fixture
def token():
    return Token("42", DEFAULT_TOKEN_EXPIRES_IN)


@fixture
def client_with_token(client, token):
    client.cached_token = token
    yield client
