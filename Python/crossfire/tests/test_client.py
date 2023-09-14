from datetime import datetime, timedelta
from unittest.mock import patch

from decouple import UndefinedValueError
from pytest import raises

from crossfire.client import (
    Client,
    CredentialsNotFoundError,
    IncorrectCrdentialsError,
    Token,
    UnknownFormatError,
)

AUTH_LOGIN_DATA = {
    "data": {
        "accessToken": "fourty-two",
        "expiresIn": 3600,
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


def test_client_initiates_with_credentials_from_kwargs():
    credentials_kwargs = {"email": "email.kwargs", "password": "password.kwargs"}
    client = Client(**credentials_kwargs)
    assert client.email == "email.kwargs"
    assert client.password == "password.kwargs"


def test_client_returns_a_token_when_cached_token_is_valid(client_with_token):
    assert client_with_token.token == "42"


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


def test_client_requests_gets_new_token_from_api(client):
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
    client.cached_token = Token("42", -3600)
    with patch("crossfire.client.post") as mock:
        mock.return_value.json.return_value = AUTH_LOGIN_DATA
        client.token  # tries to access the API to get the token
        mock.assert_called_once_with(
            "https://api-service.fogocruzado.org.br/api/v2/auth/login",
            json={"email": client.email, "password": client.password},
        )


def test_client_inserts_auth_header_on_http_get(client_with_token):
    with patch("crossfire.client.get") as mock:
        client_with_token.get("my-url")
        mock.assert_called_once_with("my-url", headers={"Authorization": "Bearer 42"})


def test_client_inserts_auth_header_on_http_get_without_overwriting(client_with_token):
    with patch("crossfire.client.get") as mock:
        client_with_token.get("my-url", headers={"answer": "fourty-two"})
        mock.assert_called_once_with(
            "my-url", headers={"Authorization": "Bearer 42", "answer": "fourty-two"}
        )


def test_client_load_states(client_with_token):
    with patch("crossfire.client.get") as mock:
        mock.return_value.json.return_value = {
            "data": [{"id": "42", "name": "Rio de Janeiro"}]
        }
        states = client_with_token.states()
        mock.assert_called_once_with(
            "https://api-service.fogocruzado.org.br/api/v2/states",
            headers={"Authorization": "Bearer 42"},
        )
        assert states.shape == (1, 2)
        assert states.name[0] == "Rio de Janeiro"


def test_client_load_states_raises_format_error(client_with_token):
    with patch("crossfire.client.get") as mock:
        mock.return_value.json.return_value = {"data": []}
        with raises(UnknownFormatError):
            client_with_token.states(format="parquet")


def test_client_load_states_as_dictionary(client_with_token):
    with patch("crossfire.client.get") as mock:
        mock.return_value.json.return_value = {
            "data": [{"id": "42", "name": "Rio de Janeiro"}]
        }
        states = client_with_token.states(format="dict")
        mock.assert_called_once_with(
            "https://api-service.fogocruzado.org.br/api/v2/states",
            headers={"Authorization": "Bearer 42"},
        )
        assert len(states) == 1
        assert states[0]["name"] == "Rio de Janeiro"
