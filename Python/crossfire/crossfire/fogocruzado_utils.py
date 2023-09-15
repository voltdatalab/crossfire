import logging
from functools import lru_cache

from crossfire.client import Client


@lru_cache(maxsize=1)
def load_client():
    return Client()


def extract_data_api(link):
    """
    Extract data from occurrences in Fogo Cruzado's API
    :param link: string
        Request the API url with search parameters

    :return: pandas.DataFrame
        Result from the request API in pandas DataFrame format
    """
    logging.info("Extracting data from Fogo Cruzado's API...")
    client = load_client()
    return client.get(link)


def extract_cities_api():
    """
    Extract data from cities in Fogo Cruzado's API

    :return: pandas.DataFrame
        Result from the request API in pandas DataFrame format
    """
    return extract_data_api("https://api.fogocruzado.org.br/api/v1/cities")
