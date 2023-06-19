from typing import Protocol


class Interface(Protocol):
    def run(self):
        pass
