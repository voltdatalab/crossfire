import json
import os
from warnings import warn

import requests
from pandas import DataFrame, json_normalize


API_URL = "https://api-service.fogocruzado.org.br/api/v2/"


def fogocruzado_key():
    """
    # Get Fogo Cruzado's API from user and password informed in fogocruzado_signin()
    :return: string
        Fogo Cruzado's API key
    """

    try:
        key = os.environ["FOGO_CRUZADO_API_TOKEN"]
    except KeyError:
        raise warn(
            (
                "There's no key available. Please check your sign-in information."
                "If you haven't included an authorized e-mail and password in this python session yet,"
                "please do so using the fogocruzado_signin() function"
            ),
            Warning,
        )
    else:
        return key


def get_token_fogocruzado():
    """
    Get token from Fogo Cruzado's API
    :raises:
    Exception
        If credentials do not correspond to Fogo Cruzado's records.
    """

    try:
        post_fogocruzado = requests.post(
            f"{API_URL}auth/login",  # todo usar urllib?
            data={
                "email": os.getenv("FOGO_CRUZADO_EMAIL"),
                "password": os.getenv("FOGO_CRUZADO_PASSWORD"),
            },
        )
        post_fogocruzado.raise_for_status()

    except requests.exceptions.HTTPError:
        raise warn(
            (
                "These credentials do not correspond to Fogo Cruzado's records."
                "Please check your e-mail and password or access https://api.fogocruzado.org.br/register to register."
            ),
            Warning,
        )

    access_fogocruzado = (
        json.loads(post_fogocruzado.content).get("data").get("accessToken")
    )
    accesstoken_fogocruzado = f"Bearer {access_fogocruzado}"
    os.environ["FOGO_CRUZADO_API_TOKEN"] = accesstoken_fogocruzado


def extract_data_api(link):  # todo remove link parameter?
    """
    Extract data from occurrences in Fogo Cruzado's API
    :param link: string
        Request the API url with search parameters

    :return: pandas.DataFrame
        Result from the request API in pandas DataFrame format
    """
    warn(("Extracting data from Fogo Cruzado's API." "..."), Warning)
    headers = {"Authorization": fogocruzado_key()}
    fogocruzado_request = requests.get(
        url=f"{API_URL}occurrences", headers=headers  # todo usar urllib?
    )

    banco = json.loads(fogocruzado_request.content)
    banco = DataFrame(banco)
    return banco


def get_cities_api():  # todo add parameters to filter https://api.fogocruzado.org.br/docs/endpoint/cities#exemplos-de-uso
    """
    Get data from cities in Fogo Cruzado's API

    :return: pandas.DataFrame
        Result from the request API in pandas DataFrame format
    """

    warn(("Extracting data from Fogo Cruzado's API." "..."), Warning)
    headers = {"Authorization": fogocruzado_key()}
    fogocruzado_cities = requests.get(
        url=f"{API_URL}cities", headers=headers  # todo usar urllib?
    )
    cities = json.loads(fogocruzado_cities.content).get("data")
    cities = json_normalize(cities)
    return cities


def get_states_api():
    """
    Get state data from Fogo Cruzado's API

    :return: pandas.DataFrame
        Result from the request API in pandas DataFrame format
    """

    warn(("Extracting data from Fogo Cruzado's API." "..."), Warning)
    headers = {"Authorization": fogocruzado_key()}
    fogocruzado_states = requests.get(
        url=f"{API_URL}states", headers=headers  # todo usar urllib?
    )
    states = json.loads(fogocruzado_states.content).get("data")
    states = DataFrame(states)
    return states
