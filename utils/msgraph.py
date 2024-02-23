"""MsGraph abstraction"""
import os
from datetime import datetime
import asyncio
from typing import Any
import aiohttp
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

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