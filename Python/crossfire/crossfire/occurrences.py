from queue import Empty, Queue
from urllib.parse import urlencode

from crossfire.errors import CrossfireError

TYPE_OCCURRENCES = {"all", "withVictim", "withoutVictim"}


class UnknownTypeOccurrenceError(CrossfireError):
    def __init__(self, type_occurrence):
        message = ("""Unknown type_occurrence""",)
        f"`{type_occurrence}`. Valid formats are: {', '.join(TYPE_OCCURRENCES)}"
        super().__init__(message)


class Occurrences:
    def __init__(
        self,
        client,
        id_state,
        id_cities=None,
        limit=None,
        format=None,
        type_occurrence="all",
    ):
        self.client = client
        self.format = format
        self.limit = limit
        if type_occurrence and type_occurrence not in TYPE_OCCURRENCES:
            raise UnknownTypeOccurrenceError(type_occurrence)

        self.buffer = Queue()
        self.next_page = 1
        self.yielded = 0

        self.params = {"idState": id_state, "typeOccurrence": type_occurrence}
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

    @property
    def url(self):
        params = urlencode(self.params, doseq=True)
        return f"{self.client.URL}/occurrences?{params}"

    def load_occurrences(self):
        if not self.next_page:
            return

        self.params["page"] = self.next_page
        occurrences, metadata = self.client.get(self.url)

        for occurrence in occurrences:
            self.buffer.put(occurrence)

        if metadata.has_next_page:
            self.next_page += 1
        else:
            self.next_page = None
