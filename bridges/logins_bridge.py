

from datetime import datetime, timezone
from bridges import Bridge
from queries.last_login_date import last_login_date


class LoginsBridge(Bridge):
    def __init__(self) -> None:
        super().__init__(120)

    async def update_data(self):
        """Connects to msgraph API and returns the `audit_logs` info"""

        index = "logs-ms_singins"
        start_date = datetime.now()
        end_date = last_login_date(self.elk.es)
        print(f"Logins: Last update date {end_date}")

        url = "https://graph.microsoft.com/v1.0/auditLogs/signIns"
        url_filter = f"$filter=createdDateTime ge {end_date.strftime(
            "%Y-%m-%dT%H:%M:%SZ")} and createdDateTime le {start_date.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}"

        await self.elk.bulk_docs((await self.mg.query(f"{url}?{url_filter}"))[0], index)


bridge = LoginsBridge()
