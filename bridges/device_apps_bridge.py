import asyncio
from typing import Any
from bridges import Bridge


class DeviceAppsBridge(Bridge):
    "Device apps bridge"

    def __init__(self) -> None:
        super().__init__("ms_device_apps")

    async def update_data(self):
        "Loads all the data of the installed applications per device using ms_graph"

        def tuple_to_dict(tuple_list: list[tuple[str, Any]]) -> dict[str, Any]:
            "Converts a tuple (str, Any) to a dict"
            return dict((key, value) for key, value in tuple_list)
        
        if self.mg and self.elk:
            # Getting all the devices with MsGraph
            devices = list((await self.mg.query("https://graph.microsoft.com/v1.0/deviceManagement/managedDevices/"))[0])

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
                device_apps, success = await self.mg.query(f'https://graph.microsoft.com/beta/deviceManagement/managedDevices/{device_id}/detectedApps')
                in_while = 0
                if (device_apps == []):
                    print(f"{self.index}: EMPTY LIST", success)
                while (not success):
                    print(f"{self.index}: In while ({
                        in_while+1}) {device_id} {device["emailAddress"]}")
                    await asyncio.sleep(5)
                    device_apps, success = await self.mg.query(f'https://graph.microsoft.com/beta/deviceManagement/managedDevices/{device_id}/detectedApps')
                    in_while += 1
                
                # For each app, parse the device information
                for device_app in device_apps:
                    device_app["deviceDetails"] = device
                    apps.append(device_app)
                print(f"{self.index}: Device ({index}/{len(devices)})")
                await asyncio.sleep(1)

            await self.elk.bulk_docs(apps, self.index)

bridge = DeviceAppsBridge()