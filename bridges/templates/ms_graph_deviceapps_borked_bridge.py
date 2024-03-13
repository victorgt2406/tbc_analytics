import asyncio
from typing import Any, Type
from bridges.templates import MsGraphBridge
from connectors import Saver


class MsGraphDeviceAppsBridge(MsGraphBridge[Saver]):
    "Device apps bridge"

    def __init__(self, saver:Type[Saver]) -> None:
        super().__init__("ms_device_apps", saver)

    async def update_data(self):
        "Loads all the data of the installed applications per device using ms_graph"

        def tuple_to_dict(tuple_list: list[tuple[str, Any]]) -> dict[str, Any]:
            "Converts a tuple (str, Any) to a dict"
            return dict((key, value) for key, value in tuple_list)
        
        if self.fetcher and self.saver:
            # Getting all the devices with MsGraph
            devices = list(await self.fetcher.fetch_data("https://graph.microsoft.com/v1.0/deviceManagement/managedDevices/"))

            # The device fields to keep
            device_fields = self.config.get("device_fields", ["id", "deviceName", "userId", "userDisplayName", "emailAddress"])
            
            # Devices cleanning
            devices = list(map(lambda x: tuple_to_dict(
                list(map(lambda y: (y, x[y]), device_fields))), devices))
            
            # All apps from all the devices
            apps = []
            for index, device in enumerate(devices):
                device_id = device["id"]

                # Getting all the apps per device
                device_apps = await self.fetcher.fetch_data(f'https://graph.microsoft.com/beta/deviceManagement/managedDevices/{device_id}/detectedApps')

                # TO DO 
                # in_while = 0
                # if (device_apps == []):
                #     print(f"{self.name}: EMPTY LIST", success)
                # while (not success):
                #     print(f"{self.name}: In while ({
                #         in_while+1}) {device_id} {device["emailAddress"]}")
                #     await asyncio.sleep(5)
                #     device_apps = await self.fetcher.fetch_data(f'https://graph.microsoft.com/beta/deviceManagement/managedDevices/{device_id}/detectedApps')
                #     in_while += 1
                
                # For each app, parse the device information
                for device_app in device_apps:
                    device_app["deviceDetails"] = device
                    apps.append(device_app)
                print(f"{self.name}: Device ({index}/{len(devices)})")
                await asyncio.sleep(1)

            await self.saver.save_data(apps, self.name) # Hay que cambiar el id de las apps a id_app_id_device