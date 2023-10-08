from queue import Empty, Queue
from urllib.parse import urlencode


class Occurrences:
    def __init__(self, client, id_state, id_cities=None, format=None):
        self.client = client
        self.format = format

        self.buffer = Queue()
        self.next_page = 1

        self.params = {
            key: value
            for key, value in {"idState": id_state, "idCities": id_cities}.items()
            if value
        }

    def __iter__(self):
        return self

    def __next__(self):
        if self.buffer.empty():
            if not self.next_page:
                raise StopIteration
            self.load_occurrences()

        try:
            occurrence = self.buffer.get_nowait()
        except Empty:
            raise StopIteration

        return occurrence

    def load_occurrences(self):
        if not self.next_page:
            return

        self.params["page"] = self.next_page
        occurrences, has_next_page = self.client.get(
            f"{self.client.URL}/occurrences?{urlencode(self.params)}"
        )

        for occurrence in occurrences:
            self.buffer.put(occurrence)

        if has_next_page:
            self.next_page += 1
        else:
            self.next_page = None
