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
            occurrences = self.buffer.get_nowait()
        except Empty:
            raise StopIteration

        return occurrences

    def load_occurrences(self):
        occurrences = self.client.get(
            "https://api-service.fogocruzado.org.br/api/v2/occurrences?"
        )
        if occurrences.get("pageMeta", {}).get("hasNextPage"):
            return self.client.get(
                "https://api-service.fogocruzado.org.br/api/v2/occurrences?"
            )

        return self.buffer.put(occurrences.get("data"))
