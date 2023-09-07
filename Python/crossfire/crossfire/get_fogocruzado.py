from datetime import date
from warnings import warn

from crossfire.fogocruzado_utils import extract_data_api, get_token_fogocruzado
from dateutil.relativedelta import relativedelta
from geopandas import GeoDataFrame, points_from_xy
from pandas import to_numeric


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
        warn(
            (
                "The interval between the initial and final date cannot be "
                "longer than 210 days (7 months). Please check your inputs."
            ),
            Warning,
        )

    else:
        banco = extract_data_api(
            link=(
                "https://api.fogocruzado.org.br/api/v1/occurrences"
                f"?data_ocorrencia[gt]={initial_date}"
                f"&data_ocorrencia[lt]={final_date}"
            )
        )
        banco_geo = GeoDataFrame(
            banco,
            geometry=points_from_xy(
                banco.longitude_ocorrencia, banco.latitude_ocorrencia
            ),
            crs="EPSG:4326",
        )

        if type(banco_geo) != GeoDataFrame:
            warn("Renovating token...", Warning)
            get_token_fogocruzado()
            banco = extract_data_api(
                link=f"https://api.fogocruzado.org.br/api/v1/occurrences?data_ocorrencia[gt]={initial_date}&data_ocorrencia[lt]={final_date}"
            )
            banco_geo = GeoDataFrame(
                banco,
                geometry=points_from_xy(
                    banco.longitude_ocorrencia, banco.latitude_ocorrencia
                ),
                crs="EPSG:4326",
            )

        else:
            banco.densidade_demo_cidade = to_numeric(banco.densidade_demo_cidade)

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

        # banco.densidade_demo_cidade = banco.densidade_demo_cidade.astype(str)

        return banco_geo
