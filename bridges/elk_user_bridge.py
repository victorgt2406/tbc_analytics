"""
User Bridge extends Bridge abstract class

By Víctor Gutiérrez Tovar
"""

from bridges import Bridge
from queries.last_user_login_date import last_user_login_date
from utils.compare_str_dates import compare_str_dates
from utils.is_x_percent_done import is_x_percent_done


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
        urls = [
            "https://graph.microsoft.com/v1.0/users",
            "https://graph.microsoft.com/v1.0/users?$select=id,assignedLicenses,userType,userPrincipalName,accountEnabled,department,usageLocation,country"
        ]

        # Fecth data from Msgraph and upload it to Elasticsearch
        for url in urls:
            data = await self.mg.fetch_data(url)
            await self.elk.save_data(data, self.name)

        mg_licenses = self.config.get("licenses", {})
        users = (await self.mg.fetch_data("https://graph.microsoft.com/v1.0/users?$select=id,assignedLicenses"))
        es = self.elk.es

        lastest_conections_docs = []
        for i, user in enumerate(users):
            if is_x_percent_done(i, len(users), 10):
                print(f"INFO: User bridge last_login transform {
                      i+1}/{len(users)}")

            user_id = user["id"]

            last_signin_interactive: str = last_user_login_date(
                user_id, es, "logs-ms_signins_interactive")
            last_signin_noninteractive: str = last_user_login_date(
                user_id, es, "logs-ms_signins_noninteractive")
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
        await self.elk.save_data(lastest_conections_docs, self.name)


bridge = UserBridge()
