"""
Elk and MsGraph manager

By Víctor Guitérrez Tovar
"""

import asyncio
from codecs import ignore_errors
from datetime import datetime, timezone
from utils.config import load_config
from utils.elk import Elk
from utils.msgraph import Msgraph

BASIC_DATA = [
    {
        "url": "https://graph.microsoft.com/v1.0/users",
        "index": "ms-users"
    },
    {
        "url": "https://graph.microsoft.com/v1.0/deviceAppManagement/mobileApps",
        "index": "ms-apps"
    },
    {
        "url": "https://graph.microsoft.com/v1.0/deviceManagement/managedDevices",
        "index": "ms-devices"
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

    async def update_logins(self):
        """Connects to msgraph API and returns the `audit_logs` info"""
        index = "logs-ms-singins"
        now = datetime.now()
        # now = datetime(2024,2,2)
        try:
            last_update = self.elk.es.search(
                index=index,
                size = 0, 
                aggs = {
                    "latestDate": {
                    "max": {
                        "field": "createdDateTime"
                    }
                    }
                }
            ).body.aggs.latestDate.value_as_string
            last_update = datetime.strptime(last_update, "%Y-%m-%dT%H:%M:%S.%sZ")
        except Exception as e:
            print("Error por la cara", e)
            last_update = datetime(2023,11,1)

        # last_update = datetime.strptime(last_update, "%Y-%m-%dT%H:%M:%S.%sZ")

        print(f"Last update date {last_update}")
        url = "https://graph.microsoft.com/v1.0/auditLogs/signIns"
        url_filter = f"$filter=createdDateTime ge {last_update.strftime("%Y-%m-%dT%H:%M:%SZ")} and createdDateTime le {now.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%sZ")}"

        await self.elk.bulk_docs(await self.ms_graph.query(f"{url}?{url_filter}"), index)

    async def auto_update_basicdata(self):
        """Auto update ms graph basic data to elasticsearch"""
        sleep_time:int = load_config().get("sleep", {}).get("basicData", 30)
        print("Auto-update: basicdata started")
        while True:
            await self.update_basicdata()
            await asyncio.sleep(sleep_time*60)

    async def auto_update_logins(self):
        """Auto update ms graph logins to elasticsearch"""
        sleep_time:int = load_config().get("sleep", {}).get("logins", 5)
        print("Auto-update: logins started")
        while True:
            await self.update_logins()
            await asyncio.sleep(sleep_time*60)