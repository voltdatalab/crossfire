import json
import os
import warnings
import requests


def fogocruzado_key():
    """
    # Get Fogo Cruzado's API from user and password informed in fogocruzado_signin()
    :return: Fogo Cruzado's API key
    """
    try:
        key = os.getenv("FOGO_CRUZADO_API_TOKEN")
    except not key:
        raise warnings.warn("There's no key available. Please check your sign-in information.\nIf you haven't included an authorized e-mail and password in this R session yet, please do so using the fogocruzado_signin() function")
    return key


def get_token_fogocruzado():
    """
    Get token from Fogo Cruzado's API
    """
    try:
        post_fogocruzado = requests.post(
            "https://api.fogocruzado.org.br/api/v1/auth/login",
            data={'email': os.getenv("FOGO_CRUZADO_EMAIL"),
                  'password': os.getenv("FOGO_CRUZADO_PASSWORD")}
        )
        post_fogocruzado.raise_for_status()

    except requests.exceptions.HTTPError:
        raise warnings.warn(
            "These credentials do not correspond to Fogo Cruzado's records. \nPlease check your e-mail and password or access https://api.fogocruzado.org.br/register to register.")

    access_fogocruzado = json.loads(post_fogocruzado.content).get('access_token')
    accesstoken_fogocruzado = f"Bearer {access_fogocruzado}"
    os.environ["FOGO_CRUZADO_API_TOKEN"] = accesstoken_fogocruzado

def extract_data_api(link):
    """
    Extract data from occurrences in Fogo Cruzado's API
    :param link:
    :return:
    """
    print("\nExtracting data from Fogo Cruzado's API.\n \n...\n")
    headers = {'Authorization': fogocruzado_key()}
    fogocruzado_request = requests.get(
        url=link,
        headers=headers)

    fogocruzado_request.encoding = "utf8"
    banco = json.loads(fogocruzado_request.content)
    return banco

def extract_cities_api():
    print("\nExtracting data from Fogo Cruzado's API.\n \n...\n")
    headers = {'Authorization': fogocruzado_key()}
    fogocruzado_cities = requests.get(
        url="https://api.fogocruzado.org.br/api/v1/cities",
        headers=headers)
    fogocruzado_cities.encoding = "utf8"
    banco = json.loads(fogocruzado_cities.content)
    return banco

# todo confirm raises menssage?

