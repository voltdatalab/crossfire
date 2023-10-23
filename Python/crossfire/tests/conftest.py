from contextlib import contextmanager
from unittest.mock import AsyncMock, Mock, patch

from httpx import AsyncClient
from pytest import fixture

from crossfire.client import Client, Token

DEFAULT_TOKEN_EXPIRES_IN = 3600
TOKEN = Token("42", DEFAULT_TOKEN_EXPIRES_IN)


@contextmanager
def async_respond_with(method_name, data):
    """The async client from `httpx` have HTTP methods that are async functions, but
    the `json` method from responses are not. This context manager wraps a async mock
    for HTTP methods and regular mocks for the `json` call."""
    mock = Mock()
    mock.json.return_value = data
    with patch.object(AsyncClient, method_name, new_callable=AsyncMock) as method:
        method.return_value = mock
        yield method


@fixture
def client():
    with patch("crossfire.client.config") as mock:
        mock.side_effect = ("email", "password")
        client = Client()
        client.URL = "http://127.0.0.1/api/v2"
        yield client


@fixture
def token_client_and_post_mock(client):
    data = {
        "data": {
            "accessToken": "fourty-two",
            "expiresIn": 3600,
        },
    }
    with async_respond_with("post", data) as post:
        yield (client, post)


@fixture
def client_with_token(client):
    client.cached_token = TOKEN
    yield client


@fixture
def client_and_get_mock(client_with_token):
    with async_respond_with("get", {}) as get:
        yield (client_with_token, get)


@fixture
def client_and_post_mock(client_with_token):
    with async_respond_with("post", {}) as post:
        yield (client_with_token, post)


@fixture
def state_client_and_get_mock(client_with_token):
    data = {"data": [{"id": "42", "name": "Rio de Janeiro"}]}
    with async_respond_with("get", data) as get:
        yield (client_with_token, get)


@fixture
def city_client_and_get_mock(client_with_token):
    data = {
        "data": [
            {
                "id": "21",
                "name": "Rio de Janeiro",
                "state": {
                    "id": "42",
                    "name": "Estado da Guanabara",
                },
            }
        ]
    }
    with async_respond_with("get", data) as get:
        yield (client_with_token, get)


@fixture
def occurrences_client_and_get_mock(client_with_token):
    data = {
        "pageMeta": {"hasNextPage": False, "pageCount": 1},
        "data": [
            {
                "id": "a7bfebed-ce9c-469d-a656-924ed8248e95",
                "latitude": "-8.1576367000",
                "longitude": "-34.9696372000",
            },
        ],
    }
    with async_respond_with("get", data) as get:
        yield (client_with_token, get)
