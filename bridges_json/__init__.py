from abc import ABC, abstractmethod
import asyncio
from connectors.json_filesystem import JsonFilesystem
from connectors.msgraph import Msgraph
from utils.config import load_config


class Bridge(ABC):
    """
    Abstract class of bridge
    """

    def __init__(self, name: str) -> None:
        self._stop = False
        self.name = name
        self.jsonfs: JsonFilesystem = JsonFilesystem()
        self.mg: Msgraph = Msgraph()
        config: dict = load_config().get("bridges", {})
        self.config: dict = config.get(name, {})
        if not self.config:
            print(f"WARNING: Bridge with name {name} has an empty configuration.")

        self.sleep: float = self.config.get("sleep", 3600)

    def start(self):
        "Start automatic mode"
        self._stop = False
        asyncio.create_task(self.automatic_mode())

    def stop(self):
        "Stop automatic mode"
        self._stop = True

    def setup(self):
        "Update the credentials of Msgraph"
        self.mg = Msgraph()
        self.jsonfs = JsonFilesystem()

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
                print(f"ERROR automatic_mode {self.name} -- {e}")

    async def run_once(self):
        "Runs one update data"
        self.setup()
        await self.update_data()

class BasicBridge(Bridge):
    "Basic Brige"

    def __init__(self, urls: list[str], name: str) -> None:
        self.urls = urls
        self.name = name
        super().__init__(name)

    async def update_data(self):
        if self.jsonfs and self.mg:
            for url in self.urls:
                await self.jsonfs.upsert_docs((await self.mg.query(url))[0], self.name)
        else:
            print("BasicBridge: ERROR JsonFileSystem or MsGraph are None")
