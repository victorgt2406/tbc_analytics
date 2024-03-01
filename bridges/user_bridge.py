from bridges import Bridge
from queries.last_user_login_date import last_user_login_date
from utils.config import load_config

URLS = ["https://graph.microsoft.com/v1.0/users",
        "https://graph.microsoft.com/v1.0/users?$select=id,assignedLicenses,userType,userPrincipalName,accountEnabled,department,usageLocation,country"]
INDEX = "ms_users"
SLEEP = 600


class UserBridge(Bridge):
    def __init__(self) -> None:
        super().__init__(SLEEP)
    async def update_data(self):
        if self.elk and self.mg and self.elk.es:
            mg_licenses = load_config()["indices"]["users"]["licenses"]
            for url in URLS:
                await self.elk.bulk_docs((await self.mg.query(url))[0], INDEX)
            users = (await self.mg.query("https://graph.microsoft.com/v1.0/users?$select=id,assignedLicenses"))[0]
            es = self.elk.es
            lastest_conections_docs = []
            for user in users:
                user_id = user["id"]
                last_singin:str = last_user_login_date(user_id, es)

                licenses = user["assignedLicenses"]
                for license in licenses:
                    if license["skuId"] in mg_licenses:
                        license["name"] = mg_licenses[license["skuId"]]


                doc = {"id": user_id, "last_singin": last_singin, "assignedLicenses": licenses}
                lastest_conections_docs.append(doc)
            await self.elk.bulk_docs(lastest_conections_docs, INDEX)

        else:
            print("BasicBridge: ERROR ELK or MSGRAPH are None")


bridge = UserBridge()
