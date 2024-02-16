"""MsGraph abstraction"""

import asyncio
import os
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
        self.headers = None
        self.users = []
        self.devices = []
        self.mobile_apps = []

    def setup_msgraph_conection(self):
        """
        Connects to microsoft to get the token to do queries at MsGraph.
        Then it saves at headers attribute the headers for the api queries
        """
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
        self.headers = {'Authorization': f'Bearer {token}'}  # token microsoft

    async def setup_msgraph_connection_async(self):
        """
        Asynchronously connects to Microsoft to get the token for queries at MsGraph.
        Then it saves at headers attribute the headers for the API queries.
        """
        load_dotenv()
        client_id = os.getenv("MS_CLIENT_ID")
        client_secret = os.getenv("MS_CLIENT_SECRET")
        tenant_id = os.getenv("MS_TENANT_ID")
        token_endpoint = f"https://login.microsoftonline.com/{
            tenant_id}/oauth2/v2.0/token"
        scope = "https://graph.microsoft.com/.default"

        # Prepare the data for the token request
        data = {
            'client_id': client_id,
            'scope': scope,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(token_endpoint, data=data) as response:
                if response.status == 200:
                    token_res = await response.json()
                    token: str = token_res.get("access_token")  # type: ignore
                    self.headers = {'Authorization': f'Bearer {token}'}
                    print(self.headers)
                else:
                    # Handle error
                    print(f"Failed to acquire token: {response.status}")

    async def query(self, graph_url: str):
        """Connects to msgraph API to return all the data request it"""

        async with aiohttp.ClientSession() as session:
            async with session.get(graph_url) as response:
                res_json = await response.json()
                return res_json

    async def async_init(self):
        """
        Does the async start
        """
        await self.setup_msgraph_connection_async()
        await self.update_users()
        await self.update_mobile_apps()
        await self.update_devices()

    async def update_users(self):
        """Connects to msgraph API to update the `users` info"""
        res = await self.query("https://graph.microsoft.com/v1.0/users")
        print(res)
        self.users = list(res["value"])

    async def update_mobile_apps(self):
        """Connects to msgraph API to update the `mobile apps` info"""
        res = await self.query("https://graph.microsoft.com/v1.0/deviceAppManagement/mobileApps")
        self.mobile_apps = list(res["value"])

    async def update_devices(self):
        """Connects to msgraph API to update the `devices` info"""
        res = await self.query("https://graph.microsoft.com/v1.0/deviceManagement/managedDevices")
        self.devices = list(res["value"])
