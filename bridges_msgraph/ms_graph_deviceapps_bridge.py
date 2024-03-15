import asyncio
from typing import Type
from bridges_msgraph.ms_graph_bridge import MsGraphBridge
from connectors import Saver
from utils.is_x_percent_done import is_x_percent_done


class MsGraphDeviceAppsBridge(MsGraphBridge[Saver]):
    "Device apps bridge"

    def __init__(self, saver: Type[Saver]) -> None:
        super().__init__("ms_device_apps", saver)

    async def update_data(self):
        "Loads all the data of the installed applications per device using ms_graph"
        # The device fields to keep
        device_fields = self.config.get("device_fields", [
                                        "id", "deviceName", "userId", "userDisplayName", "emailAddress"])

        devices = await self.fetcher.fetch_data("https://graph.microsoft.com/v1.0/deviceManagement/managedDevices/")

        # Transformation
        devices = list(map(
            lambda device: {field: device.get(
                field, None) for field in device_fields},
            devices
        ))

        # All apps from all the devices
        apps = []
        for i, device in enumerate(devices):
            device_id = device["id"]

            # Getting all the apps per device
            device_apps = await self.fetcher.fetch_data(f'https://graph.microsoft.com/beta/deviceManagement/managedDevices/{device_id}/detectedApps')

            # Save device info in all apps
            for device_app in device_apps:
                device_app["id"] = f"{device["id"]}--{device_app["id"]}"
                device_app["deviceDetails"] = device
                apps.append(device_app)

            if is_x_percent_done(i, len(devices), 1):
                print(f"""INFO: Apps bridge {
                      self.name}: Device {(i+1/len(devices))*100}% - ({i+1}/{len(devices)})""")
            await asyncio.sleep(1)

        # Hay que cambiar el id de las apps a id_app_id_device
        await self.saver.save_data(apps, self.name)
