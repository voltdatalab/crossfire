from unittest.mock import patch

from crossfire import cities, client, occurrences, states


def test_client_returns_a_single_instance():
    with patch("crossfire.clients.config"):
        client1, client2 = client(), client()

    assert id(client1) == id(client2)


def test_states_with_default_args():
    with patch("crossfire.client") as mock:
        states()
        mock.return_value.states.assert_called_once_with(format=None)


def test_states_with_custom_args():
    with patch("crossfire.client") as mock:
        states(format="df")
        mock.return_value.states.assert_called_once_with(format="df")


def test_cities_with_default_args():
    with patch("crossfire.client") as mock:
        cities()
        mock.return_value.cities.assert_called_once_with(
            city_id=None, city_name=None, state_id=None, format=None
        )


def test_cities_with_custom_args():
    with patch("crossfire.client") as mock:
        cities(city_id="42", city_name="Rio de Janeiro", state_id="21", format="df")
        mock.return_value.cities.assert_called_once_with(
            city_id="42", city_name="Rio de Janeiro", state_id="21", format="df"
        )


def test_occurrences_with_default_args():
    with patch("crossfire.client") as mock:
        occurrences("42")
        mock.return_value.occurrences.assert_called_once_with(
            "42",
            id_cities=None,
            type_occurrence="all",
            max_parallel_requests=None,
            format=None,
        )


def test_occurrences_with_custom_args():
    with patch("crossfire.client") as mock:
        occurrences(
            "42",
            id_cities=[1, 2, 3],
            type_occurrence="without",
            max_parallel_requests=10,
            format="df",
        )
        mock.return_value.occurrences.assert_called_once_with(
            "42",
            id_cities=[1, 2, 3],
            type_occurrence="without",
            max_parallel_requests=10,
            format="df",
        )
