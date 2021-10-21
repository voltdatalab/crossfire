import json
import os
from warnings import warn

import requests
from pandas import DataFrame


def fogocruzado_key():
    """
    # Get Fogo Cruzado's API from user and password informed in fogocruzado_signin()
    :return: string
        Fogo Cruzado's API key
    """

    try:
        key = os.getenv("FOGO_CRUZADO_API_TOKEN")
    except not key:
        raise warn(
            ("There's no key available. Please check your sign-in information."
             "If you haven't included an authorized e-mail and password in this python session yet,"
             "please do so using the fogocruzado_signin() function"),
            Warning)
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
            "https://api.fogocruzado.org.br/api/v1/auth/login",
            data={'email': os.getenv("FOGO_CRUZADO_EMAIL"),
                  'password': os.getenv("FOGO_CRUZADO_PASSWORD")}
        )
        post_fogocruzado.raise_for_status()

    except requests.exceptions.HTTPError:
        raise warn(
            ("These credentials do not correspond to Fogo Cruzado's records."
             "Please check your e-mail and password or access https://api.fogocruzado.org.br/register to register."),
            Warning)

    access_fogocruzado = json.loads(post_fogocruzado.content).get('access_token')
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
    warn(
        ("Extracting data from Fogo Cruzado's API."
         "..."),
        Warning)
    headers = {'Authorization': fogocruzado_key()}
    fogocruzado_request = requests.get(
        url=link,
        headers=headers)

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

    warn(
        ("Extracting data from Fogo Cruzado's API."
         "..."),
        Warning)
    headers = {'Authorization': fogocruzado_key()}
    fogocruzado_cities = requests.get(
        url="https://api.fogocruzado.org.br/api/v1/cities",
        headers=headers)
    fogocruzado_cities.encoding = "utf8"
    banco = json.loads(fogocruzado_cities.content)
    banco = DataFrame(banco)
    return banco
