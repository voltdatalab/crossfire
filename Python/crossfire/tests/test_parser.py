from geopandas import GeoDataFrame
from pandas import DataFrame
from pytest import mark, raises

from crossfire.parser import (
    IncompatibleDataError,
    RetryAfterError,
    UnknownFormatError,
    parse_response,
)


class DummyResponse:
    DATA = [{"answer": 42}]
    GEODATA = [{"answer": 42, "latitude_ocorrencia": 4, "longitude_ocorrencia": 2}]

    def __init__(self, geo, has_next_page, status_code):
        self.geo = geo
        self.has_next_page = has_next_page
        self.status_code = status_code
        if status_code == 429:
            self.headers = {"retry-after": 42}

    def json(self):
        data = self.GEODATA if self.geo else self.DATA
        return {"pageMeta": {"hasNextPage": self.has_next_page}, "data": data}


class DummyClient:
    def __init__(self, geo=False, has_next_page=False, status_code=200):
        self.response = DummyResponse(
            geo=geo, has_next_page=has_next_page, status_code=status_code
        )

    @parse_response
    async def get(self, *args, **kwargs):
        return self.response


@mark.asyncio
async def test_parse_response_raises_error_for_unknown_format():
    client = DummyClient()
    with raises(UnknownFormatError):
        await client.get(format="parquet")


@mark.asyncio
async def test_parse_response_uses_dict_by_default():
    client = DummyClient()
    data, _ = await client.get()
    assert isinstance(data, list)
    for obj in data:
        assert isinstance(obj, dict)


@mark.asyncio
async def test_parse_response_handles_metadata():
    paginated = DummyClient(has_next_page=True)
    _, metadata = await paginated.get()
    assert metadata.has_next_page

    not_paginated = DummyClient()
    _, metadata = await not_paginated.get()
    assert not metadata.has_next_page


@mark.asyncio
async def test_parse_response_uses_dataframe_when_specified():
    client = DummyClient()
    data, _ = await client.get(format="df")
    assert isinstance(data, DataFrame)


@mark.asyncio
async def test_parse_response_uses_geodataframe_when_specified():
    client = DummyClient(geo=True)
    data, _ = await client.get(geo=True, format="geodf")
    assert isinstance(data, GeoDataFrame)


@mark.asyncio
async def test_parse_response_raises_error_when_missing_coordinates():
    client = DummyClient()
    with raises(IncompatibleDataError):
        await client.get(geo=True, format="geodf")


@mark.asyncio
async def test_parse_response_raises_error_for_too_many_requests():
    client = DummyClient(status_code=429)
    with raises(RetryAfterError):
        await client.get()
