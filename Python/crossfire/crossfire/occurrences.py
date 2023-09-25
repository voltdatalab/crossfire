from queue import Queue, Empty
import random


class Occurrences:
    def __init__(self, client):
        self.client = client
        self.buffer = Queue()

    def __iter__(self):
        return self

    def __next__(self):  # __next__ takes no argument, see https://docs.python.org/3/library/stdtypes.html#iterator.__next__
        if self.buffer.empty():
            self.load_occurrences()

        try:
            occurrence = self.buffer.get_nowait()
        except Empty:
            occurrence = None
            raise StopIteration  # as mentioned above

        return occurrence

    def load_occurrences(self):
        return self.buffer.put(random.random())
