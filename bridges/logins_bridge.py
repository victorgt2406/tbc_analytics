

from datetime import datetime, timezone
from bridges import Bridge
from queries.last_login_date import last_login_date


class LoginsBridge(Bridge):
    def __init__(self) -> None:
        super().__init__("log-ms_singins")

    async def update_data(self):
        """
        Connects to msgraph API to get the auditlog logins data and updates it to Elasticsearch

        1. Get the data throw MsGraph
        2. Transform the data to save createdDateTime as @timestamp
        3. Save it in Elasticsearch
        """
        if self.elk and self.elk.es is not None and self.mg:
            index = "logs-ms_singins"
            start_date = datetime.now()
            end_date = last_login_date(self.elk.es)
            print(f"Logins: Last update date {end_date}")

            url = "https://graph.microsoft.com/v1.0/auditLogs/signIns"
            url_filter = f"$filter=createdDateTime ge {end_date.strftime(
                "%Y-%m-%dT%H:%M:%SZ")} and createdDateTime le {start_date.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}"

            # Saves to bulk_docs the data from msgraph using the url and the filter with a transformer to add @timestamp
            await self.elk.bulk_docs(list(map(lambda x: {**x, "@timestamp": x["createdDateTime"]}, (await self.mg.query(f"{url}?{url_filter}"))[0])), index)

            end_date = datetime(2024,2,1)

            url = "https://graph.microsoft.com/beta/auditLogs/signIns"
            url_filter = f"$filter=signInEventTypes/any(t: t eq 'nonInteractiveUser') and createdDateTime ge {end_date.strftime(
                "%Y-%m-%dT%H:%M:%SZ")} and createdDateTime le {start_date.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}"

            await self.elk.bulk_docs(list(map(lambda x: {**x, "@timestamp": x["createdDateTime"]}, (await self.mg.query(f"{url}?{url_filter}"))[0])), index)


bridge = LoginsBridge()
