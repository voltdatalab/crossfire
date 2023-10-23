from geopandas import GeoDataFrame
from pandas import DataFrame
from pandas.testing import assert_frame_equal
from pytest import mark, raises

from crossfire.occurrences import Accumulator, Occurrences, UnknownTypeOccurrenceError


def dummy_response(total_pages, last_page):
    if total_pages == 1:
        last_page = True

    return {
        "pageMeta": {"hasNextPage": not last_page, "pageCount": total_pages},
        "data": [
            {
                "id": "a7bfebed-ce9c-469d-a656-924ed8248e95",
                "latitude": "-8.1576367000",
                "longitude": "-34.9696372000",
            },
            {
                "id": "a14d18dd-b28f-4c30-af07-5fa40d88b3f7",
                "latitude": "-7.9800434000",
                "longitude": "-35.0553350000",
            },
        ],
    }


def test_occurrences_accumulator_for_lists():
    accumulator = Accumulator()
    accumulator.merge([1])
    accumulator.merge([2], [3])
    assert accumulator() == [1, 2, 3]


def test_occurrences_accumulator_for_df():
    accumulator = Accumulator()
    accumulator.merge(DataFrame([{"a": 1}]))
    accumulator.merge(DataFrame([{"a": 2}]), DataFrame([{"a": 3}]))
    assert_frame_equal(accumulator(), DataFrame([{"a": 1}, {"a": 2}, {"a": 3}]))


def test_occurrences_accumulator_for_geodf():
    accumulator = Accumulator()
    accumulator.merge(GeoDataFrame([{"a": 1}]))
    accumulator.merge(GeoDataFrame([{"a": 2}]), GeoDataFrame([{"a": 3}]))
    assert_frame_equal(accumulator(), GeoDataFrame([{"a": 1}, {"a": 2}, {"a": 3}]))


@mark.asyncio
async def test_occurrences_with_mandatory_parameters(occurrences_client_and_get_mock):
    client, mock = occurrences_client_and_get_mock
    mock.return_value.json.side_effect = (
        dummy_response(2, False),
        dummy_response(2, True),
    )
    occurrences = Occurrences(client, id_state="42")
    assert len(await occurrences()) == 4


@mark.asyncio
async def test_occurrences_url_with_mandatory_parameters(
    occurrences_client_and_get_mock,
):
    client, mock = occurrences_client_and_get_mock
    occurrences = Occurrences(client, id_state=42)
    await occurrences()
    mock.assert_called_once_with(
        "http://127.0.0.1/api/v2/occurrences?idState=42&typeOccurrence=all&page=1",
        headers={"Authorization": "Bearer 42"},
    )


@mark.asyncio
async def test_occurrences_url_with_id_cities_parameters(
    occurrences_client_and_get_mock,
):
    client, mock = occurrences_client_and_get_mock
    occurrences = Occurrences(client, id_state="42", id_cities="21")
    await occurrences()
    mock.assert_called_once_with(
        "http://127.0.0.1/api/v2/occurrences?idState=42&typeOccurrence=all&idCities=21&page=1",
        headers={"Authorization": "Bearer 42"},
    )


@mark.asyncio
async def test_occurrences_url_with_two_id_cities_parameters(
    occurrences_client_and_get_mock,
):
    client, mock = occurrences_client_and_get_mock
    occurrences = Occurrences(client, id_state="42", id_cities=["21", "11"])
    await occurrences()
    mock.assert_called_once_with(
        "http://127.0.0.1/api/v2/occurrences?idState=42&typeOccurrence=all&idCities=21&idCities=11&page=1",
        headers={"Authorization": "Bearer 42"},
    )


@mark.asyncio
async def test_occurrences_with_victims(occurrences_client_and_get_mock):
    client, mock = occurrences_client_and_get_mock
    occurrences = Occurrences(client, id_state=42, type_occurrence="withVictim")
    await occurrences()
    mock.assert_called_once_with(
        "http://127.0.0.1/api/v2/occurrences?idState=42&typeOccurrence=withVictim&page=1",
        headers={"Authorization": "Bearer 42"},
    )


@mark.asyncio
async def test_occurrences_without_victims(occurrences_client_and_get_mock):
    client, mock = occurrences_client_and_get_mock
    occurrences = Occurrences(client, id_state=42, type_occurrence="withoutVictim")
    await occurrences()
    mock.assert_called_once_with(
        "http://127.0.0.1/api/v2/occurrences?idState=42&typeOccurrence=withoutVictim&page=1",
        headers={"Authorization": "Bearer 42"},
    )


def test_occurrence_raises_error_for_unkown_occurrence_type():
    with raises(UnknownTypeOccurrenceError):
        Occurrences(None, id_state="42", type_occurrence="42")
