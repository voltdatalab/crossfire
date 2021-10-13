import warnings
from datetime import date
from dateutil.relativedelta import relativedelta
from pandas import DataFrame
from geopandas import GeoDataFrame, points_from_xy
from Python.fogocruzado_utils import extract_data_api, get_token_fogocruzado


def get_fogocruzado(city = None,
                    initial_date = date.today()-relativedelta(months=6),
                    final_date = date.today(),
                    state = ["PE", "RJ"],
                    security_agent = [0,1]):
  if (final_date - initial_date).days >= 210:
    warnings.warn("The interval between the initial and final date cannot be longer than 210 days (7 months). Please check your inputs.")
  else:
      banco = extract_data_api(
        link = f"https://api.fogocruzado.org.br/api/v1/occurrences?data_ocorrencia[gt]={initial_date}&data_ocorrencia[lt]={final_date}"
      )

      banco = DataFrame(banco)
      banco_geo = GeoDataFrame(
        banco,
        geometry=points_from_xy(
          banco.longitude_ocorrencia,
          banco.latitude_ocorrencia)
      )

  if type(banco_geo) != 'geopandas.geodataframe.GeoDataFrame':

    warnings.showwarning("Renovating token...")
    get_token_fogocruzado()
    banco = extract_data_api(
      link=f"https://api.fogocruzado.org.br/api/v1/occurrences?data_ocorrencia[gt]={initial_date}&data_ocorrencia[lt]={final_date}"
    )

    banco = DataFrame(banco)
    banco_geo = GeoDataFrame(
      banco,
      geometry=points_from_xy(
        banco.longitude_ocorrencia,
        banco.latitude_ocorrencia)
    )
  else
    pass
  # banco.cod_ibge_cidade <- as.character(banco$cod_ibge_cidade)
  # banco$cod_ibge_estado <- as.character(banco$cod_ibge_estado)
  # banco$densidade_demo_cidade <- as.numeric(banco$densidade_demo_cidade)

  # if(!is.null(city)){

    # banco <- banco %>%
    #   dplyr::filter(.data$nome_cidade %in% city,
    #                 .data$uf_estado %in% state,
    #                 .data$presen_agen_segur_ocorrencia %in% security_agent)
  #
  # } else
  #
  #   banco <- banco %>%
  #     dplyr::filter(.data$uf_estado %in% state,
  #                   .data$presen_agen_segur_ocorrencia %in% security_agent)
  #
  return banco
