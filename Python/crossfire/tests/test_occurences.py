from unittest.mock import Mock

from crossfire.occurrences import Occurrences


def dummy_response(last_page=False):
    return {
        "pageMeta": {
            "hasNextPage": not last_page,
        },
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


def test_occurrences_from_at_least_two_pages():
    client = Mock()
    client.get.return_value.json.return_value = dummy_response()
    generator = Occurrences(client)
    occurrences = tuple(occ for count, occ in enumerate(generator, 1) if count <= 3)
    assert client.get.call_count == 2
    assert len(occurrences) == 3


def test_occurrences_stops_when_there_are_no_more_pages():
    client = Mock()
    client.get.return_value.json.side_effect = (
        dummy_response(False),
        dummy_response(True),
    )
    occurrences = tuple(occurence for occurence in Occurrences(client))
    assert client.get.call_count == 2
    assert len(occurrences) == 4
