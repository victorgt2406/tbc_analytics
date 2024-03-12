"Bridges"

from abc import ABC, abstractmethod
import time
import asyncio
from connectors.elk import Elk
from connectors.msgraph import Msgraph
from utils.config import load_config


class Bridge(ABC):
    """
    Abstract class of bridge
    """

    def __init__(self, name: str) -> None:
        self._stop = False
        self.name = name
        self.setup()
        config: dict = load_config().get("bridges", {})
        self.fail_sleep = config.get("fail_sleep", 1)
        self.config: dict = config.get(name, {})
        if not self.config:
            print(f"WARNING: Bridge with index {
                  name} has an empty configuration.")

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
                start_time = time.time()
                await self.update_data()
                end_time = time.time()

                total_time = end_time - start_time
                print(f"INFO: Bridge {self.name}: took {total_time:.2f} secs")
                await asyncio.sleep(self.sleep)
            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"ERROR automatic_mode {self.name} -- {e}")
                await asyncio.sleep(self.fail_sleep)

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
        for url in self.urls:
            await self.elk.save_data(
                data=await self.mg.fetch_data(url),
                place=self.index
            )
