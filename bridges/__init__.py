"Bridges"

from abc import ABC, abstractmethod
import time
import asyncio
from typing import Type
from connectors import Fetcher, Saver
from connectors.elk import Elk
from connectors.json_filesystem import JsonFilesystem
from connectors.msgraph import Msgraph
from utils.config import load_config


class Bridge(ABC):
    """
    Abstract class of bridge
    """

    def __init__(self, name: str, fetcher_class: Type[Fetcher], saver_class: Type[Saver]) -> None:

        self.name = name
        # Fetcher
        self.fetcher_class: Type[Fetcher] = fetcher_class
        self.fetcher: Fetcher = self.fetcher_class()
        # Saver
        self.saver_class: Type[Saver] = saver_class
        self.saver: Saver = self.saver_class()

        # Config
        config: dict = load_config().get("bridges", {})
        self.fail_sleep = config.get("fail_sleep", 1)
        self.config: dict = config.get(name, {})
        self._stop = False

        self.sleep: float = self.config.get("sleep", 3600)

    def setup(self):
        "Update the credentials to Elasticsearch and Msgraph"
        self.saver = self.saver_class()
        self.fetcher = self.fetcher_class()

    def start(self):
        "Start automatic mode"
        self._stop = False
        asyncio.create_task(self.automatic_mode())

    def stop(self):
        "Stop automatic mode"
        self._stop = True

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