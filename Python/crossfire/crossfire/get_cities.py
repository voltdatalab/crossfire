from crossfire.fogocruzado_utils import extract_cities_api
from pandas import DataFrame, to_numeric


def get_cities():
    """
    extracts data about cities covered by Fogo Cruzado's project,
    from its API.
    The function returns a pandas DataFrame where each observation corresponds to a city.
    :return: pandas.DataFrame
    """
    banco = extract_cities_api()

    if type(banco) is not DataFrame:
        fogocruzado_signin()  # Does it make sense? Shouldn't be get_token_fogocruzado()?
        banco = extract_cities_api()

    banco.DensidadeDemografica = to_numeric(banco.DensidadeDemografica)

    return (banco)
