"MSGraph Basic Bridge template"

from typing import List, Type
from bridges import Bridge
from connectors import Saver
from connectors.elk import Elk
from connectors.json_filesystem import JsonFilesystem
from connectors.msgraph import Msgraph


class MsGraphBasicBridge(Bridge):
    """
    MsGraph Basic Bridge
    """

    def __init__(self, urls: List[str], name: str, saver_class: Type[Saver]) -> None:
        super().__init__(name, Msgraph, saver_class)
        self.urls = urls
        self.index = name

    async def update_data(self):
        for url in self.urls:
            await self.saver.save_data(
                data=await self.fetcher.fetch_data(url),
                place=self.index
            )


class MsGraphElkBasicBridge(MsGraphBasicBridge):
    """
    MsGraph Basic Bridge using Elasticsearch
    """
    def __init__(self, urls: List[str], name: str) -> None:
        super().__init__(urls, name, Elk)


class MsGraphJsonBasicBridge(MsGraphBasicBridge):
    """
    MsGraph Basic Bridge using Json File System
    """
    def __init__(self, urls: List[str], name: str) -> None:
        super().__init__(urls, name, JsonFilesystem)
