from bridges_msgraph import MsGraphElkBridgeBasic


URLS = ["https://graph.microsoft.com/v1.0/deviceManagement/managedDevices"]
INDEX = "ms_devices"
bridge = MsGraphElkBridgeBasic(URLS,INDEX)
