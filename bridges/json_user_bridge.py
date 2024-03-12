"""
User Bridge extends Bridge abstract class

By Víctor Gutiérrez Tovar
"""

from bridges_json import Bridge
from queries_json.last_user_login_date import last_user_login_date
from utils.compare_str_dates import compare_str_dates

URLS = ["https://graph.microsoft.com/v1.0/users",
        "https://graph.microsoft.com/v1.0/users?$select=id,assignedLicenses,userType,userPrincipalName,accountEnabled,department,usageLocation,country"]
SLEEP = 600


class UserBridge(Bridge):
    """
    User Bridge: updates the user data
    - basic data
    - licenses per user
    - last login interactive
    - last login non interactive
    """

    def __init__(self) -> None:
        super().__init__("ms_users")

    async def update_data(self):
        if self.jsonfs and self.mg:
            mg_licenses = self.config.get("licenses", {})
            for url in URLS:
                await self.jsonfs.upsert_docs((await self.mg.query(url))[0], self.name)
            users = (await self.mg.query("https://graph.microsoft.com/v1.0/users?$select=id,assignedLicenses"))[0]
            lastest_conections_docs = []
            for user in users:
                user_id = user["id"]
                last_signin_interactive: str = await last_user_login_date(
                    user_id, self.jsonfs, "logs-ms_signins_interactive")
                last_signin_noninteractive: str = await last_user_login_date(
                    user_id, self.jsonfs, "logs-ms_signins_noninteractive")
                last_signin = last_signin_interactive if compare_str_dates(
                    last_signin_interactive, last_signin_noninteractive) else last_signin_noninteractive

                licenses = user["assignedLicenses"]
                for l in licenses:
                    if l["skuId"] in mg_licenses:
                        l["name"] = mg_licenses[l["skuId"]]

                doc = {
                    "id": user_id,
                    "last_signin_interative": last_signin_interactive,
                    "assignedLicenses": licenses,
                    "last_signin_noninteractive": last_signin_noninteractive,
                    "last_signin": last_signin
                }
                lastest_conections_docs.append(doc)
            await self.jsonfs.upsert_docs(lastest_conections_docs, self.name)

        else:
            print("UserBridge: ERROR MSGRAPH or JsonFileSystem are None")


bridge = UserBridge()
