from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

L = TypeVar('L') # List type
P = TypeVar('P') # Place to store it or upload it


class Connector(ABC):
    "Connector"
    def __init__(self, name="unnamed connector") -> None:
        self.name = name
        self.set_up()
        if name == "unnamed connector":
            print("WARNING: Unnamed connector")
        else:
            print(f"Connector: {name} RUNNING...")

    @abstractmethod
    def set_up(self):
        """Prepares the Fetcher or Saver to fetch_data"""


class Fetcher(Connector, ABC, Generic[L, P]):
    "Connector that can fetch data"
    @abstractmethod
    async def fetch_data(self, place:P, **args) -> List[L]:
        """Gets some data from a source and return it"""

class Saver(Connector, ABC, Generic[L, P]):
    "Connector that save data"
    @abstractmethod
    async def save_data(self, data:List[L], place:P, **args) -> None:
        """Gets some data from a source and return it"""

class FectcherSaver(Fetcher[L,P], Saver[L,P], ABC, Generic[L, P]):
    "Connector that can fetch and save data"