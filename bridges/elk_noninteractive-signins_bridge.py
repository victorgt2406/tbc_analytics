
"""
Non Interactive Signings Bridge

By Víctor Gutiérrez Tovar
"""
from datetime import datetime, timezone
from bridges.templates import MsGraphElkBridge
from queries.last_login_date import last_login_date


class NonInteractiveSigninsBridge(MsGraphElkBridge):
    "Non Interactive Sigins from MsGraph auditlogs"

    def __init__(self) -> None:
        super().__init__("logs-ms_signins_noninteractive")

    async def update_data(self):
        """
        Connects to msgraph API to get the auditlog of the non Interactive signins. 
        Then, updates it to Elasticsearch

        1. Get the data throw MsGraph
        2. Transform the data to save createdDateTime as @timestamp
        3. Save it in Elasticsearch
        """

        end_date = datetime.now()  # Date at the moment
        start_date = last_login_date(self.saver.es, self.name)  # last date of a login stored
        print(f"INFO NonInteractiveSignins: Last update date {start_date}")

        # MsGraph Query
        url = "https://graph.microsoft.com/beta/auditLogs/signIns"
        url_filter = f"$filter=signInEventTypes/any(t: t eq 'nonInteractiveUser') and createdDateTime ge {start_date.strftime(
            "%Y-%m-%dT%H:%M:%SZ")} and createdDateTime le {end_date.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}"

        # Get data from MsGraph
        data = await self.fetcher.fetch_data(f"{url}?{url_filter}")

        # Store data to Elasticsearch
        await self.saver.save_data(
            data=list(map(
                # Unnecesary transform, very slow TODO
                lambda x: {**x, "@timestamp": x["createdDateTime"]},
                data
            )),
            place=self.name
        )


bridge = NonInteractiveSigninsBridge()
