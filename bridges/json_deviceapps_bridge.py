from bridges.templates import MsGraphDeviceAppsBridge
from connectors.json_filesystem import JsonFilesystem

bridge = MsGraphDeviceAppsBridge(JsonFilesystem)