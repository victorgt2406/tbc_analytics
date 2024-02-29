from bridges import Bridge
from queries.last_user_login_date import last_user_login_date

URLS = ["https://graph.microsoft.com/v1.0/users",
        "https://graph.microsoft.com/v1.0/users?$select=id,assignedLicenses"]
INDEX = "ms_users"
SLEEP = 600


class UserBridge(Bridge):
    def __init__(self) -> None:
        super().__init__(SLEEP)
    async def update_data(self):
        if self.elk and self.mg and self.elk.es:
            for url in URLS:
                await self.elk.bulk_docs((await self.mg.query(url))[0], INDEX)
            users = (await self.mg.query("https://graph.microsoft.com/v1.0/users"))[0]
            es = self.elk.es
            lastest_conections_docs = []
            for user in users:
                user_id = user["id"]
                last_singin:str = last_user_login_date(user_id, es)
                doc = {"id": user_id, "last_singin": last_singin}
                lastest_conections_docs.append(doc)
            await self.elk.bulk_docs(lastest_conections_docs, INDEX)

        else:
            print("BasicBridge: ERROR ELK or MSGRAPH are None")


bridge = UserBridge()
