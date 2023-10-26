from dataclasses import dataclass
from re import compile

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
from crossfire.logger import Logger

FORMATS = {"df", "dict", "geodf"}
CRS = "EPSG:4326"

logger = Logger(__name__)


class UnknownFormatError(CrossfireError):
    def __init__(self, format):
        message = f"Unknown format `{format}`. Valid formats are: {', '.join(FORMATS)}"
        super().__init__(message)


class IncompatibleDataError(CrossfireError):
    pass


class RetryAfterError(Exception):
    def __init__(self, retry_after):
        self.retry_after = retry_after
        message = (
            "Got HTTP Status 429 Too Many Requests. "
            f"Retry after {self.retry_after} seconds"
        )
        super().__init__(message)


def to_geo_dataframe(df):
    if not {"latitude_ocorrencia", "longitude_ocorrencia"}.issubset(df.columns):
        raise IncompatibleDataError(
            "Missing columns `latitude_ocorrencia` and `longitude_ocorrencia`. "
            "They are needed to create a GeoDataFrame."
        )

    geometry = points_from_xy(df.longitude_ocorrencia, df.latitude_ocorrencia)
    return GeoDataFrame(df, geometry=geometry, crs=CRS)


@dataclass
class Metadata:
    page: int
    take: int
    item_count: int
    page_count: int
    has_previous_page: bool
    has_next_page: bool

    SNAKE_CASE_REGEX = compile("([A-Z])")

    @classmethod
    def to_snake_case(cls, name):
        return cls.SNAKE_CASE_REGEX.sub(r"_\1", name).lower()

    @classmethod
    def from_response(cls, response):
        kwargs = {
            cls.to_snake_case(key): value
            for key, value in response.get("pageMeta", {}).items()
        }
        for key in cls.__dataclass_fields__.keys() - kwargs.keys():
            kwargs[key] = None
        return cls(**kwargs)


def parse_response(method):
    async def wrapper(self, *args, **kwargs):
        """Converts API response to a dictionary, Pandas DataFrame or GeoDataFrame."""
        format = kwargs.pop("format", None)
        if format and format not in FORMATS:
            raise UnknownFormatError(format)

        response = await method(self, *args, **kwargs)
        if response.status_code == 429:
            try:
                wait = int(response.headers.get("retry-after") or 1)
            except ValueError:
                wait = 1
            raise RetryAfterError(wait)

        try:
            contents = response.json()
        except:
            logger.error(
                "Failed to decode response as JSON (HTTP Status "
                f"{response.status_code} {response.url} {response.headers}): {response.text}"
            )
            raise

        metadata = Metadata.from_response(contents)
        data = contents.get("data", [])

        if HAS_GEOPANDAS and format == "geodf":
            return to_geo_dataframe(DataFrame(data)), metadata

        if HAS_PANDAS and format == "df":
            return DataFrame(data), metadata

        return data, metadata

    return wrapper
