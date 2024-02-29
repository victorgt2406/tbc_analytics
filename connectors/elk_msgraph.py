"""
Elk and MsGraph manager

By Víctor Guitérrez Tovar
"""

import asyncio
from datetime import datetime, timezone
from typing import Any
from utils.config import load_config
from connectors.elk import Elk
from connectors.msgraph import Msgraph
from queries.last_login_date import last_login_date

BASIC_DATA = [
    {
        "url": "https://graph.microsoft.com/v1.0/users",
        "index": "ms_users"
    },
    {
        "url": "https://graph.microsoft.com/v1.0/users?$select=id,assignedLicenses",
        "index": "ms_users"
    },
    {
        "url": "https://graph.microsoft.com/v1.0/deviceAppManagement/mobileApps",
        "index": "ms_apps"
    },
    {
        "url": "https://graph.microsoft.com/v1.0/deviceManagement/managedDevices",
        "index": "ms_devices"
    }
]


class ElkMsgraph:
    """
    A class that abstract Elasticsearch to be used with msgraph easierly

    Attributes:
        `es`: Client of Elasticsearch.
    Methods:
        `to_esdocs`,
        `bulk_docs`

    """

    def __init__(self) -> None:
        self.elk = Elk()
        self.mg = Msgraph()

    async def update_basicdata(self):
        """updates the basic values of ms_graph"""
        for data in BASIC_DATA:
            await self.elk.bulk_docs((await self.mg.query(data["url"]))[0], data["index"])

    async def update_logins(self, start_date:datetime|None = None, end_date:datetime|None=None):
        """Connects to msgraph API and returns the `audit_logs` info"""
        index = "logs-ms_singins"
        if(start_date is None):
            start_date = datetime.now()
        if(not end_date):
            end_date = last_login_date(self.elk.es)

        print(f"Logins: Last update date {end_date}")
        url = "https://graph.microsoft.com/v1.0/auditLogs/signIns"
        url_filter = f"$filter=createdDateTime ge {end_date.strftime(
            "%Y-%m-%dT%H:%M:%SZ")} and createdDateTime le {start_date.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}"

        await self.elk.bulk_docs((await self.mg.query(f"{url}?{url_filter}"))[0], index)

    async def update_deviceapps(self):
        """
        Loads all the data of the installed applications per device using ms_graph
        """
        def tuple_to_dict(tuple_list:list[tuple[str,Any]])->dict[str, Any]:
            return dict((key, value) for key, value in tuple_list)
        devices = list((await self.mg.query("https://graph.microsoft.com/v1.0/deviceManagement/managedDevices/"))[0])
        fields = ["id", "deviceName", "userId", "userDisplayName", "emailAddress", "operatingSystem", "osVersion", "lastSyncDateTime"]

        devices = list(map(lambda x: tuple_to_dict(list(map(lambda y: (y, x[y]), fields))), devices))
        apps = []
        for index, device in enumerate(devices):
            device_id = device["id"]
            device_apps, success = await self.mg.query(f'https://graph.microsoft.com/beta/deviceManagement/managedDevices/{device_id}/detectedApps')
            in_while = 0
            if(device_apps == []):
                print("DeviceApps: EMPTY LIST",success)
            while (not success):
                print(f"DeviceApps: In while ({in_while+1}) {device_id} {device["emailAddress"]}")
                await asyncio.sleep(30)
                device_apps, success = await self.mg.query(f'https://graph.microsoft.com/beta/deviceManagement/managedDevices/{device_id}/detectedApps')
                in_while+=1
            for device_app in device_apps:
                device_app["deviceDetails"] = device
                apps.append(device_app)
            print(f"DeviceApps: Device ({index}/{len(devices)})")
            await asyncio.sleep(1) # 0.5 sleep per device
        
        await self.elk.bulk_docs(apps, "ms_device_apps")

    async def auto_update_basicdata(self):
        """Auto update ms graph basic data to elasticsearch"""
        sleep_time: int = load_config().get("sleep", {}).get("basicData", 30)
        print("Auto-update: basicdata started")
        while True:
            await self.update_basicdata()
            # await self.update_deviceapps()
            await asyncio.sleep(sleep_time)

    async def auto_update_logins(self):
        """Auto update ms graph logins to elasticsearch"""
        sleep_time: int = load_config().get("sleep", {}).get("logins", 5)
        print("Auto-update: logins started")
        while True:
            await self.update_logins()
            await asyncio.sleep(sleep_time)
