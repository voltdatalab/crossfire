from queue import Empty, Queue


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

    def load_occurrences(self):
        occurrences, has_next_page = self.client.get(f"{self.client.URL}/occurrences")
        if has_next_page:
            return self.client.get(f"{self.client.URL}/occurrences")

        for occurrence in occurrences:
            self.buffer.put(occurrence)
