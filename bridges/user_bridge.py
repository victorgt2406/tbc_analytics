from bridges import BasicBridge

URLS = ["https://graph.microsoft.com/v1.0/users",
        "https://graph.microsoft.com/v1.0/users?$select=id,assignedLicenses"]
INDEX = "ms_users"
SLEEP = 600
bridge = BasicBridge(URLS, INDEX, SLEEP)
