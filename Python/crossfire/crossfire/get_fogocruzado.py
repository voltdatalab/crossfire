from datetime import date

from dateutil.relativedelta import relativedelta
from geopandas import GeoDataFrame, points_from_xy
from pandas import DataFrame, to_numeric

from crossfire.fogocruzado_utils import extract_data_api, get_token_fogocruzado


def get_fogocruzado(city=None,
                    initial_date=date.today() - relativedelta(months=6),
                    final_date=date.today(),
                    state=['PE', 'RJ'],
                    security_agent=[0, 1]):
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
    >>> get_crossfire(initial_date=date(2020-1-1), final_date=date(2020-3-1), state='RJ')
    """
    if (final_date - initial_date).days >= 210:
        print(
            'The interval between the initial and final date cannot be longer than 210 days (7 months). Please check your inputs.')

    else:
        banco = extract_data_api(
            link=f'https://api.fogocruzado.org.br/api/v1/occurrences?data_ocorrencia[gt]={initial_date}&data_ocorrencia[lt]={final_date}'
        )
        banco_geo = GeoDataFrame(
            banco,
            geometry=points_from_xy(
                banco.longitude_ocorrencia,
                banco.latitude_ocorrencia),
            crs="EPSG:4326"
        )

        if type(banco_geo) != GeoDataFrame:
            print('Renovating token...')
            get_token_fogocruzado()
            banco = extract_data_api(
                link=f'https://api.fogocruzado.org.br/api/v1/occurrences?data_ocorrencia[gt]={initial_date}&data_ocorrencia[lt]={final_date}'
            )
            banco_geo = GeoDataFrame(
                banco,
                geometry=points_from_xy(
                    banco.longitude_ocorrencia,
                    banco.latitude_ocorrencia),
                crs="EPSG:4326"
            )

        else:
            # banco.cod_ibge_cidade <- as.character(banco$cod_ibge_cidade)
            # banco$cod_ibge_estado <- as.character(banco$cod_ibge_estado)
            banco.densidade_demo_cidade = to_numeric(banco.densidade_demo_cidade)

        if city is not None: # should be string, not none
            banco_geo = banco_geo[banco_geo.uf_estado == city]

        banco_geo = banco_geo[banco_geo.uf_estado.isin(state)] # should be list
        banco_geo = banco_geo[banco_geo.presen_agen_segur_ocorrencia.isin(security_agent)] # should be list

        return banco_geo
