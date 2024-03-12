from datetime import datetime, timezone
from bridges_json import Bridge
from queries_json.last_login_date import last_login_date


class InteractiveSigninsBridge(Bridge):
    def __init__(self) -> None:
        super().__init__("logs-ms_signins_interactive")

    async def update_data(self):
        """
        Connects to msgraph API to get the auditlog logins data and updates it to Elasticsearch

        1. Get the data throw MsGraph
        2. Transform the data to save createdDateTime as @timestamp
        3. Save it in Elasticsearch
        """
        if self.jsonfs and self.mg:
            start_date = datetime.now()
            end_date:datetime = await last_login_date(self.jsonfs, self.name)
            print(f"INFO InteractiveSignins: Last update date {end_date}")

            url = "https://graph.microsoft.com/v1.0/auditLogs/signIns"
            url_filter = f"$filter=createdDateTime ge {end_date.strftime(
                "%Y-%m-%dT%H:%M:%SZ")} and createdDateTime le {start_date.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}"

            await self.jsonfs.upsert_docs(list(map(lambda x: {**x, "@timestamp": x["createdDateTime"]}, (await self.mg.query(f"{url}?{url_filter}"))[0])), self.name)

bridge = InteractiveSigninsBridge()
