from geopandas import GeoDataFrame
from pandas import DataFrame
from pytest import raises

from crossfire.parser import IncompatibleDataError, UnknownFormatError, parse_response


class DummyResponse:
    DATA = [{"answer": 42}]
    GEODATA = [{"answer": 42, "latitude_ocorrencia": 4, "longitude_ocorrencia": 2}]

    def __init__(self, geo):
        self.geo = geo

    def json(self):
        data = self.GEODATA if self.geo else self.DATA
        return {"data": data}


class DummyClient:
    def __init__(self, geo=False):
        self.response = DummyResponse(geo=geo)

    @parse_response
    def get(self, *args, **kwargs):
        return self.response


def test_parse_response_raises_error_for_unknown_format():
    client = DummyClient()
    with raises(UnknownFormatError):
        client.get(format="parquet")


def test_parse_response_uses_dict_by_default():
    client = DummyClient()
    data = client.get()
    assert isinstance(data, list)


def test_parse_response_uses_dataframe_when_specified():
    client = DummyClient()
    data = client.get(format="df")
    assert isinstance(data, DataFrame)


def test_parse_response_uses_geodataframe_when_specified():
    client = DummyClient(geo=True)
    data = client.get(geo=True, format="geodf")
    assert isinstance(data, GeoDataFrame)


def test_parse_response_raises_error_when_missing_coordinates():
    client = DummyClient()
    with raises(IncompatibleDataError):
        client.get(geo=True, format="geodf")
