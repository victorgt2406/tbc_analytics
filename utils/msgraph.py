"""MsGraph abstraction"""
import os
from typing import Any, List
import aiohttp
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
from datetime import datetime, timezone, timedelta
import asyncio
import json


class Msgraph:
    """
    A class that abstract all MsGraph API

    Attributes:
        headers
    """

    def __init__(self) -> None:
        """All the MsGraph opetations"""
        self.headers = self._get_headers()
        self.last_auditlogs_update: datetime | None = None

    def _get_headers(self) -> dict[str,str]:
        """Returns the headers required to connect to MsGraph"""
        load_dotenv()
        client_id = os.getenv("MS_CLIENT_ID")
        client_secret = os.getenv("MS_CLIENT_SECRET")
        tenant_id = os.getenv("MS_TENANT_ID")

        authority = f"https://login.microsoftonline.com/{tenant_id}"
        scope = ["https://graph.microsoft.com/.default"]

        ms = ConfidentialClientApplication(
            client_id, authority=authority, client_credential=client_secret)

        token_res = ms.acquire_token_for_client(scopes=scope)
        token: str = token_res.get("access_token")  # type: ignore
        return {'Authorization': f'Bearer {token}'}  # token microsoft

    async def query(self, graph_url: str) -> list[dict[str,Any]]:
        """Connects to msgraph API to return all the data request it"""
        all_data = []

        async with aiohttp.ClientSession() as session:
            while graph_url:
                async with session.get(graph_url, headers=self.headers) as response:
                    res_json = await response.json()
                    if("error" in res_json):
                        print(f"MsGraph: ERROR {graph_url} failed")
                    else:
                        print(f"MsGraph: {graph_url} runned sucesfully")
                    all_data.extend(res_json.get('value', []))
                    graph_url = res_json.get('@odata.nextLink', None)
                    await asyncio.sleep(0.2)
        return all_data       

    # async def get_users(self) -> List[dict]:
    #     """Connects to msgraph API to update the `users` info"""
    #     return await self.query("https://graph.microsoft.com/v1.0/users")

    # async def get_mobile_apps(self) -> List[dict]:
    #     """Connects to msgraph API to update the `mobile apps` info"""
    #     return await self.query("https://graph.microsoft.com/v1.0/deviceAppManagement/mobileApps")

    # async def get_devices(self) -> List[dict]:
    #     """Connects to msgraph API and returns the `devices` info"""
    #     return await self.query("https://graph.microsoft.com/v1.0/deviceManagement/managedDevices")

    # async def get_auditlogs(self) -> List[dict]:
    #     """Connects to msgraph API and returns the `audit_logs` info

    #     arreglar para hacerlo desde elasticsearch
    #     GET /mi_indice/_search
    #         {
    #         "size": 0, 
    #         "aggs": {
    #             "fecha_mas_reciente": {
    #             "max": {
    #                 "field": "fecha_creacion"
    #             }
    #             }
    #         }
    #         }
    #     """
    #     now = datetime.now()
    #     now = datetime(2024,2,2)
    #     if self.last_auditlogs_update is None:
    #         self.last_auditlogs_update = datetime(2023,12,31)
    #         # self.last_auditlogs_update = now - timedelta(days=8)
    #     url = "https://graph.microsoft.com/v1.0/auditLogs/signIns"
    #     url_filter = f"$filter=createdDateTime ge {self.last_auditlogs_update.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")} and createdDateTime le {now.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%sZ")}"
    #     self.last_auditlogs_update = now

    #     return await self.query(f"{url}?{url_filter}")
    
if __name__ == "__main__":
   pass
    # async def main():
    #     res = await Msgraph().get_auditlogs()
    #     # print(json.dumps(res))
    #     # Crear y escribir en un archivo JSON
    #     with open('./archived/logs.json', 'w') as json_file:
    #         json.dump(res,json_file, indent=4)

    #     res = await Msgraph().get_devices()
    #     # print(json.dumps(res))
    #     # Crear y escribir en un archivo JSON
    #     with open('./archived/devices.json', 'w') as json_file:
    #         json.dump(res,json_file, indent=4)
    # asyncio.run(main())