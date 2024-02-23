"""
Elk and MsGraph manager

By Víctor Guitérrez Tovar
"""

import asyncio
from datetime import datetime, timezone
from utils.config import load_config
from utils.elk import Elk
from utils.msgraph import Msgraph
from queries.last_login_date import last_login_date

BASIC_DATA = [
    {
        "url": "https://graph.microsoft.com/v1.0/users",
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
        self.ms_graph = Msgraph()
        self.config = load_config()

    async def update_basicdata(self):
        """updates the basic values of ms_graph"""
        for data in BASIC_DATA:
            await self.elk.bulk_docs(await self.ms_graph.query(data["url"]), data["index"])

    async def update_logins(self, start_date:datetime|None = None, end_date:datetime|None=None):
        """Connects to msgraph API and returns the `audit_logs` info"""
        index = "logs-ms_singins"
        if(start_date is None):
            start_date = datetime.now()
        if(end_date is None):
            end_date = last_login_date(self.elk.es)

        print(f"Logins: Last update date {end_date}")
        url = "https://graph.microsoft.com/v1.0/auditLogs/signIns"
        url_filter = f"$filter=createdDateTime ge {end_date.strftime(
            "%Y-%m-%dT%H:%M:%SZ")} and createdDateTime le {start_date.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}"

        await self.elk.bulk_docs(await self.ms_graph.query(f"{url}?{url_filter}"), index)

    async def auto_update_basicdata(self):
        """Auto update ms graph basic data to elasticsearch"""
        sleep_time: int = load_config().get("sleep", {}).get("basicData", 30)
        print("Auto-update: basicdata started")
        while True:
            await self.update_basicdata()
            await asyncio.sleep(sleep_time*60)

    async def auto_update_logins(self):
        """Auto update ms graph logins to elasticsearch"""
        sleep_time: int = load_config().get("sleep", {}).get("logins", 5)
        print("Auto-update: logins started")
        while True:
            await self.update_logins()
            await asyncio.sleep(sleep_time*60)
