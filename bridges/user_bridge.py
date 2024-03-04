"""
User Bridge extends Bridge abstract class

By Víctor Gutiérrez Tovar
"""

from bridges import Bridge
from queries.last_user_login_date import last_user_login_date

URLS = ["https://graph.microsoft.com/v1.0/users",
        "https://graph.microsoft.com/v1.0/users?$select=id,assignedLicenses,userType,userPrincipalName,accountEnabled,department,usageLocation,country"]
INDEX = "ms_users"
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
        if self.elk and self.mg and self.elk.es:
            mg_licenses = self.config.get("licenses", {})
            for url in URLS:
                await self.elk.bulk_docs((await self.mg.query(url))[0], INDEX)
            users = (await self.mg.query("https://graph.microsoft.com/v1.0/users?$select=id,assignedLicenses"))[0]
            es = self.elk.es
            lastest_conections_docs = []
            for user in users:
                user_id = user["id"]
                last_signin_interactive: str = last_user_login_date(
                    user_id, es, "logs-ms_signins_interactive")
                last_signin_noninteractive: str = last_user_login_date(
                    user_id, es, "logs-ms_signins_noninteractive")

                licenses = user["assignedLicenses"]
                for l in licenses:
                    if l["skuId"] in mg_licenses:
                        l["name"] = mg_licenses[l["skuId"]]

                doc = {
                    "id": user_id,
                    "last_signin_interative": last_signin_interactive,
                    "assignedLicenses": licenses,
                    "last_signin_noninteractive": last_signin_noninteractive
                }
                lastest_conections_docs.append(doc)
            await self.elk.bulk_docs(lastest_conections_docs, INDEX)

        else:
            print("BasicBridge: ERROR ELK or MSGRAPH are None")


bridge = UserBridge()
