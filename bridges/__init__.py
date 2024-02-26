from abc import ABC, abstractmethod
import asyncio
from connectors.elk import Elk
from connectors.msgraph import Msgraph


class Bridge(ABC):
    """
    Abstract class of bridge
    """

    def __init__(self, s_sleep: float = 3600) -> None:
        self.sleep: float = s_sleep
        self._stop = False
        self.setup()

    def start(self):
        "Start automatic mode"
        self._stop = False
        asyncio.create_task(self.automatic_mode())

    def stop(self):
        "Stop automatic mode"
        self._stop = True

    def setup(self):
        "Update the credentials to Elasticsearch and Msgraph"
        self.elk = Elk()
        self.mg = Msgraph()

    @abstractmethod
    async def update_data(self):
        ...

    async def automatic_mode(self):
        "Runs update data indefinitely ultil it is stopped"
        while not self._stop:
            await self.update_data()
            await asyncio.sleep(self.sleep)

    async def run_once(self):
        "Runs one update data"
        await self.update_data()


class BasicBridge(Bridge):
    "Basic Brige"

    def __init__(self, urls: list[str], index: str, s_sleep: float = 3600) -> None:
        self.urls = urls
        self.index = index
        super().__init__(s_sleep)

    async def update_data(self):
        for url in self.urls:
            await self.elk.bulk_docs((await self.mg.query(url))[0], self.index)