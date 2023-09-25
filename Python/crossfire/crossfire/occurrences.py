from queue import Queue, Empty
import random


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
        return self.buffer.put(random.random())
