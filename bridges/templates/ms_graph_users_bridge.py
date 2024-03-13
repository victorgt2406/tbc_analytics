from datetime import datetime
from bridges.templates import MsGraphBridge

# URLS = ["https://graph.microsoft.com/v1.0/users?$select=id,displayName,assignedLicenses,signInActivity,email,userPrincipalName"]
# NAME = "ms_usersv2"


class MsGraphUsersBridge(MsGraphBridge):
    def __init__(self, saver_class: type) -> None:
        super().__init__("ms_usersv2", saver_class)

    async def update_data(self):
        mg_users = await self.fetcher.fetch_data(
            "https://graph.microsoft.com/v1.0/users?$select=id,displayName,assignedLicenses,signInActivity,email,userPrincipalName"
        )

        def lastest_signin(doc: dict) -> str:
            # Is Non Interactive Datetime later?
            def is_non_interactive_later(non_interactive: str, interactive: str):
                ni_date = datetime.fromisoformat(non_interactive)
                i_date = datetime.fromisoformat(interactive)
                return ni_date > i_date

            # Non interactive and interactive date
            signin_activity: dict = doc.get("signInActivity", {})
            non_interactive: str | None = signin_activity.get(
                "lastNonInteractiveSignInDateTime", "1900-01-01T00:00:00Z")
            interactive: str | None = signin_activity.get(
                "lastSignInDateTime", "1900-01-01T00:00:00Z")

            # last signin is interactive datetime unless non interactive datetime is later
            last_signin = "1900-01-01T00:00:00Z"

            if interactive and non_interactive and is_non_interactive_later(non_interactive, interactive):
                last_signin = non_interactive

            return last_signin

        users = list(map(
            lambda x: {
                "signInActivity": {
                    "lastestSignInDateTime": lastest_signin(x)},
                **x
            },
            mg_users
        ))

        await self.saver.save_data(users, self.name)
