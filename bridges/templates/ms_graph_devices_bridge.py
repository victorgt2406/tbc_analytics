from bridges.templates import MsGraphBridgeBasic

URLS = ["https://graph.microsoft.com/v1.0/deviceManagement/managedDevices"]
INDEX = "ms_devices"

class MsGraphDevicesBridge(MsGraphBridgeBasic):
    def __init__(self, saver_class: type) -> None:
        super().__init__(URLS, INDEX, saver_class)
