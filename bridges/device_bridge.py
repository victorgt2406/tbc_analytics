
from bridges.templates import MsGraphElkBasicBridge


URLS = ["https://graph.microsoft.com/v1.0/deviceManagement/managedDevices"]
INDEX = "ms_devices"
bridge = MsGraphElkBasicBridge(URLS,INDEX)
