import logging

from pandas import DataFrame

from crossfire.client import Client


client = Client()


def to_dataframe(resp):
    resp.encoding = "utf8"
    return DataFrame(resp.json())


def extract_data_api(link):
    """
    Extract data from occurrences in Fogo Cruzado's API
    :param link: string
        Request the API url with search parameters

    :return: pandas.DataFrame
        Result from the request API in pandas DataFrame format
    """
    logging.info("Extracting data from Fogo Cruzado's API...")
    resp = client.get(url=link)
    return to_dataframe(resp)


def extract_cities_api():
    """
    Extract data from cities in Fogo Cruzado's API

    :return: pandas.DataFrame
        Result from the request API in pandas DataFrame format
    """
    logging.info("Extracting data from Fogo Cruzado's API...")
    resp = client.get(url="https://api.fogocruzado.org.br/api/v1/cities")
    return to_dataframe(resp)
