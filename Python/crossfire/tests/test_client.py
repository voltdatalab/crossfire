from datetime import datetime, timedelta
from unittest.mock import patch

from decouple import UndefinedValueError
from pytest import raises

from crossfire.client import (
    Client,
    Token,
    CredentialsNotFoundError,
    IncorrectCrdentialsError,
)

DEFAULT_TOKEN_EXPIRES_IN = 3600
AUTH_LOGIN_DATA = {
    "data": {
        "accessToken": "fourty-two",
        "expiresIn": DEFAULT_TOKEN_EXPIRES_IN,
    },
}


def test_client_initiates_with_proper_credentials(client):
    assert client.email == "email"
    assert client.password == "password"


def test_client_does_not_initiate_with_proper_credentials():
    with patch("crossfire.client.config") as mock:
        mock.side_effect = UndefinedValueError()
        with raises(CredentialsNotFoundError):
            Client()


def test_client_returns_a_token_when_cached_token_is_valid(client):
    client.cached_token = Token("42", DEFAULT_TOKEN_EXPIRES_IN)
    assert client.token == "42"


def test_client_access_the_api_to_generate_token(client):
    with patch("crossfire.client.post") as mock:
        mock.return_value.json.return_value = AUTH_LOGIN_DATA
        client.token  # tries to access the API to get the token
        mock.assert_called_once_with(
            "https://api-service.fogocruzado.org.br/api/v2/auth/login",
            json={"email": client.email, "password": client.password},
        )


def test_client_raises_an_error_with_wrong_crdentials(client):
    with patch("crossfire.client.post") as mock:
        mock.return_value.status_code = 401
        with raises(IncorrectCrdentialsError):
            assert client.token


def test_client_gets_new_token_from_api(client):
    with patch("crossfire.client.post") as mock:
        mock.return_value.status_code = 201
        mock.return_value.json.return_value = AUTH_LOGIN_DATA

        assert client.token == "fourty-two"
        assert client.cached_token.valid_until <= datetime.now() + timedelta(
            seconds=3600
        )


def test_client_propagates_error_when_fails_to_get_token(client):
    with patch("crossfire.client.post") as mock:
        mock.side_effect = Exception("Boom!")
        with raises(Exception) as error:
            client.token
            assert str(error.value) == "Boom!"


def test_client_goes_back_to_the_api_when_token_is_expired(client):
    client.cached_token = Token("42", -DEFAULT_TOKEN_EXPIRES_IN)
    with patch("crossfire.client.post") as mock:
        mock.return_value.json.return_value = AUTH_LOGIN_DATA
        client.token  # tries to access the API to get the token
        mock.assert_called_once_with(
            "https://api-service.fogocruzado.org.br/api/v2/auth/login",
            json={"email": client.email, "password": client.password},
        )
