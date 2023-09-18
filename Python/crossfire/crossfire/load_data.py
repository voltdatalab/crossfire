from functools import lru_cache
from datetime import date

from dateutil.relativedelta import relativedelta

from crossfire.client import Client


@lru_cache(maxsize=1)
def load_client():
    return Client()


class InvalidDateIntervalError(Exception):
    def __init__(self, start_date, end_date):
        delta = end_date - start_date
        message = (
            "The interval between the initial and final date cannot be "
            f"longer than 210 days (7 months). The interval between {start_date} "
            f"and {end_date} is {delta.days} days. Please check your inputs."
        )
        super().__init__(message)


def get_fogocruzado(
    city=None,
    initial_date=date.today() - relativedelta(months=6),
    final_date=date.today(),
    state=["PE", "RJ"],
    security_agent=[0, 1],
):
    """
    :param city: string
    :param initial_date: datetime.date
        Initial searching date
    :param final_date: date.time
        final searching date
    :param state: list with string, by default ['PE', 'RJ']

    :param security_agent: list with int, by default [0, 1]
    :return:
    gpd.GeoDataFrame
        crossfire occurrences and metadata
    :example:
    >>> from crossfire import crossfire_signin, get_crossfire
    >>> from datetime import date
    >>> crossfire_signin(email='user@host.com', password='password')
    >>> get_crossfire(
    ...     initial_date=date(2020-1-1),
    ...     final_date=date(2020-3-1),
    ...     state='RJ'
    ... )
    """
    if (final_date - initial_date).days >= 210:
        raise InvalidDateIntervalError(initial_date, final_date)

    url = (
        "https://api.fogocruzado.org.br/api/v1/occurrences"
        f"?data_ocorrencia[gt]={initial_date}"
        f"&data_ocorrencia[lt]={final_date}"
    )
    client = load_client()
    banco_geo = client.get(url, format="geodf")

    if isinstance(city, str):
        city = [city]

    if isinstance(city, list):
        banco_geo = banco_geo[banco_geo.nome_cidade.isin(city)]

    if isinstance(state, str):
        state = [state]

    if isinstance(state, list):
        banco_geo = banco_geo[banco_geo.uf_estado.isin(state)]

    if isinstance(security_agent, int):
        security_agent = [security_agent]

    if isinstance(security_agent, list):
        banco_geo = banco_geo[
            banco_geo.presen_agen_segur_ocorrencia.isin(security_agent)
        ]

    return banco_geo
