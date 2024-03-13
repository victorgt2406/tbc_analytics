"""
MsGraph abstraction

by Víctor Gutiérrez Tovar
"""
import os
import asyncio
from typing import Any, Dict, List
import aiohttp
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
from connectors import Fetcher

from utils.config import load_config


class Msgraph(Fetcher[Dict[str,Any], str]):
    """
    A class that abstract all MsGraph API

    Attributes:
        headers

    Methods:
        query -> allows to query a msgraph api request and return all its data
    """

    def __init__(self) -> None:
        """All the MsGraph opetations"""
        super().__init__("MsGraph")
        self.set_up()
    
    def set_up(self):
        self.headers:dict[str, str] = self._get_headers()
        self.config: dict = load_config().get("ms_graph", {})
        self.sleep: float = self.config.get("sleep", 0.2)

    async def fetch_data(self, place: str, **args) ->List[Dict[str, Any]]:
        data, succes = await self._query(place, args.get("get_all_data", True))
        if not succes:
            raise ValueError(f"ERROR: connector {self.name} failed when fetching data")
        return data

    def _get_headers(self) -> dict[str, str]:
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
        if not token:
            raise ValueError("ERROR Msgraph: token is None, CHECK .env FILE")

        return {'Authorization': f'Bearer {token}'}  # token microsoft

    async def _query(self, graph_url: str, get_all_data=True) -> tuple[list[dict[str, Any]], bool]:
        """Connects to msgraph API and returns all the data requested"""
        all_data = []
        success = True
        timeout = aiohttp.ClientTimeout(total=self.config.get("timeout", 30))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            while graph_url:
                async with session.get(graph_url, headers=self.headers) as response:
                    res_json:dict = await response.json()
                    if ("error" in res_json):
                        print(
                            f"""
                            MsGraph: ERROR {graph_url} failed\n
                            \t{res_json["error"]["code"]} -- {res_json["error"]["message"]}
                            """)
                        success = False
                    else:
                        print(f"MsGraph: {graph_url[:self.config.get("url_slicing", 50)]} runned successfully")
                    all_data.extend(res_json.get('value', []))
                    if get_all_data:
                        graph_url = res_json.get('@odata.nextLink', None)
                    else:
                        graph_url = None # type: ignore
                    await asyncio.sleep(self.sleep)
        return all_data, success
