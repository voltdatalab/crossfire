from datetime import datetime, timedelta
from unittest.mock import patch

from decouple import UndefinedValueError
from pytest import mark, raises

from crossfire.client import (
    Client,
    CredentialsNotFoundError,
    IncorrectCredentialsError,
    Token,
)
from crossfire.parser import UnknownFormatError


def test_client_initiates_with_proper_credentials(client):
    assert client.credentials["email"] == "email"
    assert client.credentials["password"] == "password"


def test_client_does_not_initiate_with_proper_credentials():
    with patch("crossfire.client.config") as mock:
        mock.side_effect = UndefinedValueError()
        with raises(CredentialsNotFoundError):
            Client()


def test_client_initiates_with_credentials_from_kwargs():
    credentials_kwargs = {"email": "email.kwargs", "password": "password.kwargs"}
    client = Client(**credentials_kwargs)
    assert client.credentials["email"] == "email.kwargs"
    assert client.credentials["password"] == "password.kwargs"


@mark.asyncio
async def test_client_returns_a_token_when_cached_token_is_valid(client_with_token):
    assert await client_with_token.token() == "42"


@mark.asyncio
async def test_client_access_the_api_to_generate_token(token_client_and_post_mock):
    client, mock = token_client_and_post_mock
    await client.token()  # tries to access the API to get the token
    mock.assert_called_once_with(
        "https://api-service.fogocruzado.org.br/api/v2/auth/login",
        json=client.credentials,
    )


@mark.asyncio
async def test_client_raises_an_error_with_wrong_credentials(client_and_post_mock):
    client, mock = client_and_post_mock
    client.cached_token = None
    mock.return_value.status_code = 401
    with raises(IncorrectCredentialsError):
        assert await client.token()


@mark.asyncio
async def test_client_requests_gets_new_token_from_api(token_client_and_post_mock):
    client, mock = token_client_and_post_mock
    mock.return_value.status_code = 201
    assert await client.token() == "fourty-two"
    assert client.cached_token.valid_until <= datetime.now() + timedelta(seconds=3600)


@mark.asyncio
async def test_client_propagates_error_when_fails_to_get_token(client_and_post_mock):
    client, mock = client_and_post_mock
    mock.side_effect = Exception("Boom!")
    with raises(Exception) as error:
        await client.token()
        assert str(error.value) == "Boom!"


@mark.asyncio
async def test_client_goes_back_to_the_api_when_token_is_expired(
    token_client_and_post_mock,
):
    client, mock = token_client_and_post_mock
    client.cached_token = Token("42", -3600)
    await client.token()  # tries to access the API to get the token
    mock.assert_called_once_with(
        "https://api-service.fogocruzado.org.br/api/v2/auth/login",
        json=client.credentials,
    )


@mark.asyncio
async def test_client_inserts_auth_header_on_http_get(client_and_get_mock):
    client, mock = client_and_get_mock
    await client.get("my-url")
    mock.assert_called_once_with("my-url", headers={"Authorization": "Bearer 42"})


@mark.asyncio
async def test_client_inserts_auth_on_http_get_without_overwriting(client_and_get_mock):
    client, mock = client_and_get_mock
    await client.get("my-url", headers={"answer": "fourty-two"})
    mock.assert_called_once_with(
        "my-url", headers={"Authorization": "Bearer 42", "answer": "fourty-two"}
    )


def test_client_load_states(state_client_and_get_mock):
    client, mock = state_client_and_get_mock
    states = client.states()
    mock.assert_called_once_with(
        "https://api-service.fogocruzado.org.br/api/v2/states",
        headers={"Authorization": "Bearer 42"},
    )
    assert len(states) == 1
    assert states[0]["name"] == "Rio de Janeiro"


def test_client_load_states_as_df(state_client_and_get_mock):
    client, mock = state_client_and_get_mock
    states = client.states(format="df")
    mock.assert_called_once_with(
        "https://api-service.fogocruzado.org.br/api/v2/states",
        headers={"Authorization": "Bearer 42"},
    )
    assert states.shape == (1, 2)
    assert states.name[0] == "Rio de Janeiro"


def test_client_load_states_raises_format_error(state_client_and_get_mock):
    client, _ = state_client_and_get_mock
    with raises(UnknownFormatError):
        client.states(format="parquet")


def test_client_load_cities(city_client_and_get_mock):
    client, mock = city_client_and_get_mock
    cities = client.cities()
    mock.assert_called_once_with(
        "https://api-service.fogocruzado.org.br/api/v2/cities?",
        headers={"Authorization": "Bearer 42"},
    )
    assert cities[0]["name"] == "Rio de Janeiro"
    assert cities[0]["state"]["name"] == "Estado da Guanabara"


def test_client_load_cities_as_dictionary(city_client_and_get_mock):
    client, mock = city_client_and_get_mock
    cities = client.cities(format="dict")
    mock.assert_called_once_with(
        "https://api-service.fogocruzado.org.br/api/v2/cities?",
        headers={"Authorization": "Bearer 42"},
    )
    assert len(cities) == 1
    assert cities[0]["name"] == "Rio de Janeiro"
    assert cities[0]["state"]["name"] == "Estado da Guanabara"


def test_client_load_cities_with_city_id(city_client_and_get_mock):
    client, mock = city_client_and_get_mock
    client.cities(city_id="21")
    mock.assert_called_once_with(
        "https://api-service.fogocruzado.org.br/api/v2/cities?cityId=21",
        headers={"Authorization": "Bearer 42"},
    )


def testclientes_with_city_name(city_client_and_get_mock):
    client, mock = city_client_and_get_mock
    client.cities(city_name="Rio de Janeiro")
    mock.assert_called_once_with(
        "https://api-service.fogocruzado.org.br/api/v2/cities?cityName=Rio+de+Janeiro",
        headers={"Authorization": "Bearer 42"},
    )


def test_client_load_cities_with_state_id(city_client_and_get_mock):
    client, mock = city_client_and_get_mock
    client.cities(state_id="42")
    mock.assert_called_once_with(
        "https://api-service.fogocruzado.org.br/api/v2/cities?stateId=42",
        headers={"Authorization": "Bearer 42"},
    )


def test_client_load_cities_with_more_than_one_params(city_client_and_get_mock):
    client, mock = city_client_and_get_mock
    client.cities(state_id="42", city_name="Rio de Janeiro")
    mock.assert_called_once_with(
        "https://api-service.fogocruzado.org.br/api/v2/cities?cityName=Rio+de+Janeiro&stateId=42",
        headers={"Authorization": "Bearer 42"},
    )
