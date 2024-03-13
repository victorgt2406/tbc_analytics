from bridges.templates import MsGraphUsersBridge
from connectors.json_filesystem import JsonFilesystem

bridge = MsGraphUsersBridge(JsonFilesystem)