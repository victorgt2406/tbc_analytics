"MsGraph Elk Bridge"

from bridges import Bridge
from connectors.elk import Elk
from connectors.msgraph import Msgraph


class MsGraphElkBridge(Bridge[Msgraph,Elk]):
    def __init__(self, name: str) -> None:
        super().__init__(name, Msgraph, Elk)