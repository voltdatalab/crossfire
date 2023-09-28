from queue import Empty, Queue
from urllib.parse import urlencode


class Occurrences:
    def __init__(self, client):
        self.client = client
        self.buffer = Queue()

    def __iter__(self):
        return self

    def __next__(self):
        if self.buffer.empty():
            self.load_occurrences()

        try:
            occurrence = self.buffer.get_nowait()
        except Empty:
            raise StopIteration

        return occurrence

    def load_occurrences(self, id_state=None, id_cities=None, format=None):
        params = {"idState": id_state, "idCities": id_cities}
        cleaned = urlencode({key: value for key, value in params.items() if value})
        occurrences, has_next_page = self.client.get(
            f"{self.client.URL}/occurrences?{cleaned}"
        )
        if has_next_page:
            pass
            # return self.client.get(f"{self.client.URL}/occurrences?{cleaned}", format)

        for occurrence in occurrences:
            self.buffer.put(occurrence)
