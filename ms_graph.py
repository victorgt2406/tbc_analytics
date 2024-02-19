"""MsGraph abstraction"""

import os
from typing import List
import aiohttp
from dotenv import load_dotenv
from msal import ConfidentialClientApplication


class Msgraph:
    """
    A class that abstract all MsGraph API

    Attributes:
        users
        devices
        mobile_devices
    """

    def __init__(self) -> None:
        """All the MsGraph opetations"""
        self.headers = self._get_headers()

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

    async def query(self, graph_url: str):
        """Connects to msgraph API to return all the data request it"""

        async with aiohttp.ClientSession() as session:
            async with session.get(graph_url, headers=self.headers) as response:
                res_json = await response.json()
                return res_json

    async def get_users(self) -> List[dict]:
        """Connects to msgraph API to update the `users` info"""
        res = await self.query("https://graph.microsoft.com/v1.0/users")
        return list(res["value"])

    async def get_mobile_apps(self) -> List[dict]:
        """Connects to msgraph API to update the `mobile apps` info"""
        res = await self.query("https://graph.microsoft.com/v1.0/deviceAppManagement/mobileApps")
        return list(res["value"])

    async def get_devices(self) -> List[dict]:
        """Connects to msgraph API and returns the `devices` info"""
        res = await self.query("https://graph.microsoft.com/v1.0/deviceManagement/managedDevices")
        return list(res["value"])

    async def get_audit_logs(self) -> List[dict]:
        """Connects to msgraph API and returns the `audit_logs` info"""
        res = await self.query("https://graph.microsoft.com/v1.0/auditLogs/signIns")
        print(res)
        return list(res["value"])
    
if __name__ == "__main__":
    import asyncio
    import json
    async def main():
        res = await Msgraph().get_audit_logs()
        print(json.dumps(res))
        # Crear y escribir en un archivo JSON
        with open('./archived/logs.json', 'w') as json_file:
            json.dump(res,json_file, indent=4)
    asyncio.run(main())