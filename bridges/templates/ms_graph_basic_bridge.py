"MSGraph Basic Bridge template"

from typing import Generic, List, Type, TypeVar
from bridges import Bridge
from connectors import Saver
from connectors.elk import Elk
from connectors.json_filesystem import JsonFilesystem
from connectors.msgraph import Msgraph

S = TypeVar('S', bound=Saver)

class MsGraphBridgeBasic(Bridge[Msgraph, S], Generic[S]):
    """
    MsGraph Basic Bridge
    """

    def __init__(self, urls: List[str], name: str, saver_class: Type[S]) -> None:
        super().__init__(name, Msgraph, saver_class)
        self.urls = urls
        self.index = name

    async def update_data(self):
        for url in self.urls:
            await self.saver.save_data(
                data=await self.fetcher.fetch_data(url),
                place=self.index
            )


class MsGraphElkBridgeBasic(MsGraphBridgeBasic[Elk]):
    """
    MsGraph Basic Bridge using Elasticsearch
    """
    def __init__(self, urls: List[str], name: str) -> None:
        super().__init__(urls, name, Elk)


class MsGraphJsonBridgeBasic(MsGraphBridgeBasic[JsonFilesystem]):
    """
    MsGraph Basic Bridge using Json File System
    """
    def __init__(self, urls: List[str], name: str) -> None:
        super().__init__(urls, name, JsonFilesystem)
