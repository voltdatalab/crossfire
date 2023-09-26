try:
    from pandas import DataFrame

    HAS_PANDAS = True
except ModuleNotFoundError:
    HAS_PANDAS = False

try:
    from geopandas import GeoDataFrame, points_from_xy

    HAS_GEOPANDAS = True
except ModuleNotFoundError:
    HAS_GEOPANDAS = False


from crossfire.errors import CrossfireError

FORMATS = {"df", "dict", "geodf"}
CRS = "EPSG:4326"


class UnknownFormatError(CrossfireError):
    def __init__(self, format):
        message = f"Unknown format `{format}`. Valid formats are: {', '.join(FORMATS)}"
        super().__init__(message)


class IncompatibleDataError(CrossfireError):
    pass


def parse_response(method):
    def wrapper(self, *args, **kwargs):
        """Converts API response to a dictionary, Pandas DataFrame or GeoDataFrame."""
        format = kwargs.pop("format", None)
        if format and format not in FORMATS:
            raise UnknownFormatError(format)

        response = method(self, *args, **kwargs)
        response.encoding = "utf8"
        contents = response.json()
        data = contents.get("data", [])

        if HAS_GEOPANDAS and format == "geodf":
            df = DataFrame(data)
            if not {"latitude_ocorrencia", "longitude_ocorrencia"}.issubset(df.columns):
                raise IncompatibleDataError(
                    "Missing columns `latitude_ocorrencia` and `longitude_ocorrencia`. "
                    "They are needed to create a GeoDataFrame."
                )

            geometry = points_from_xy(df.longitude_ocorrencia, df.latitude_ocorrencia)
            return GeoDataFrame(df, geometry=geometry, crs=CRS)

        if HAS_PANDAS and format == "df":
            return DataFrame(data)

        return data

    return wrapper
