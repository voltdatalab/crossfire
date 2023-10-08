from queue import Empty, Queue
from urllib.parse import urlencode


class Occurrences:
    def __init__(self, client, id_state, id_cities=None, limit=None, format=None):
        self.client = client
        self.format = format
        self.limit = limit

        self.buffer = Queue()
        self.next_page = 1
        self.yielded = 0

        self.params = {"idState": id_state}
        if id_cities:
            self.params["idCities"] = id_cities

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit and self.yielded >= self.limit:
            raise StopIteration

        if self.buffer.empty():
            if not self.next_page:
                raise StopIteration
            self.load_occurrences()

        try:
            occurrence = self.buffer.get_nowait()
        except Empty:
            raise StopIteration

        self.yielded += 1
        return occurrence

    def load_occurrences(self):
        if not self.next_page:
            return

        occurrences, has_next_page = self.client.get(
            f"{self.urlbase}&{urlencode({'page': self.next_page})}"
        )

        for occurrence in occurrences:
            self.buffer.put(occurrence)

        if has_next_page:
            self.next_page += 1
        else:
            self.next_page = None
