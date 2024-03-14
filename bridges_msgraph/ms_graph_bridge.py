"""
    MsGraph Bridge
    - MsGraph as Fetcher
    - It needs to have a Saver connector defined
"""
from typing import Generic, Type, TypeVar
from bridges import Bridge
from connectors import Saver
from connectors.msgraph import Msgraph

S = TypeVar('S', bound=Saver)

class MsGraphBridge(Bridge[Msgraph,Saver], Generic[S]):
    def __init__(self, name: str, saver_class: Type[S]) -> None:
        super().__init__(name, Msgraph, saver_class)