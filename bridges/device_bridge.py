from bridges import BasicBridge

URLS = ["https://graph.microsoft.com/v1.0/deviceManagement/managedDevices"]
INDEX = "ms_devices"
SLEEP = 600
bridge = BasicBridge(URLS,INDEX)
