from abc import ABC, abstractmethod
import asyncio
from connectors.elk import Elk
from connectors.msgraph import Msgraph
from utils.config import load_config


class Bridge(ABC):
    """
    Abstract class of bridge
    """

    def __init__(self, index: str) -> None:
        self._stop = False
        self.index = index
        self.elk: Elk | None = None
        self.mg: Msgraph | None = None
        config: dict = load_config().get("bridges", {})
        self.config: dict = config.get(index, {})
        if not self.config:
            print(f"WARNING: Bridge with index {index} has an empty configuration.")

        self.sleep: float = self.config.get("sleep", 3600)

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
            self.setup()
            try:
                await self.update_data()
                await asyncio.sleep(self.sleep)
            except Exception as e: # pylint: disable=broad-exception-caught
                print(f"ERROR automatic_mode {self.index} -- {e}")
                await asyncio.sleep(0.1)

    async def run_once(self):
        "Runs one update data"
        self.setup()
        await self.update_data()


class BasicBridge(Bridge):
    "Basic Brige"

    def __init__(self, urls: list[str], index: str) -> None:
        self.urls = urls
        self.index = index
        super().__init__(index)

    async def update_data(self):
        if self.elk and self.mg:
            for url in self.urls:
                await self.elk.bulk_docs((await self.mg.query(url))[0], self.index)
        else:
            print("BasicBridge: ERROR ELK or MSGRAPH are None")
