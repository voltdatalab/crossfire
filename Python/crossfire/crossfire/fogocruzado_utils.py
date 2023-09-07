import logging
import json
import os

import requests
from pandas import DataFrame


class CredentialsNotFoundError(Exception):
    def __init__(self, key):
        message = (
            f"There's no enviornment variable `{key}` available. Please "
            "check your sign-in information. If you haven't included an "
            "authorized e-mail and password in this Python session yet, "
            "please do so using the `fogocruzado_signin()` function"
        )
        super().__init__(message)


class InvalidCredentialsError(Exception):
    def __init__(self, http_error):
        message = (
            "These credentials do not correspond to Fogo Cruzado's records. "
            "Please check your e-mail and password or access "
            "https://api.fogocruzado.org.br/register to register.\n\n"
            f"Original HTTP error: {http_error}"
        )
        super().__init__(message)


def fogocruzado_key():
    """
    # Get Fogo Cruzado's API from user and password informed in fogocruzado_signin()
    :return: string
        Fogo Cruzado's API key
    """
    try:
        return os.environ["FOGO_CRUZADO_API_TOKEN"]
    except KeyError:
        raise CredentialsNotFoundError("FOGO_CRUZADO_API_TOKEN")


def get_token_fogocruzado():
    """
    Get token from Fogo Cruzado's API
    :raises:
    Exception
        If credentials do not correspond to Fogo Cruzado's records.
    """

    try:
        post_fogocruzado = requests.post(
            "https://api.fogocruzado.org.br/api/v1/auth/login",
            data={
                "email": os.getenv("FOGO_CRUZADO_EMAIL"),
                "password": os.getenv("FOGO_CRUZADO_PASSWORD"),
            },
        )
        post_fogocruzado.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise InvalidCredentialsError(error)

    access_fogocruzado = json.loads(post_fogocruzado.content).get("access_token")
    accesstoken_fogocruzado = f"Bearer {access_fogocruzado}"
    os.environ["FOGO_CRUZADO_API_TOKEN"] = accesstoken_fogocruzado


def extract_data_api(link):
    """
    Extract data from occurrences in Fogo Cruzado's API
    :param link: string
        Request the API url with search parameters

    :return: pandas.DataFrame
        Result from the request API in pandas DataFrame format
    """
    logging.info("Extracting data from Fogo Cruzado's API...")
    headers = {"Authorization": fogocruzado_key()}
    fogocruzado_request = requests.get(url=link, headers=headers)

    fogocruzado_request.encoding = "utf8"
    banco = json.loads(fogocruzado_request.content)
    banco = DataFrame(banco)
    return banco


def extract_cities_api():
    """
    Extract data from cities in Fogo Cruzado's API

    :return: pandas.DataFrame
        Result from the request API in pandas DataFrame format
    """

    logging.info("Extracting data from Fogo Cruzado's API...")
    headers = {"Authorization": fogocruzado_key()}
    fogocruzado_cities = requests.get(
        url="https://api.fogocruzado.org.br/api/v1/cities", headers=headers
    )
    fogocruzado_cities.encoding = "utf8"
    banco = json.loads(fogocruzado_cities.content)
    banco = DataFrame(banco)
    return banco
