from datetime import datetime
from connectors.json_filesystem import JsonFilesystem


async def last_login_date(jsonfs:JsonFilesystem, name:str) -> datetime:
    """
    Get the last login date
    """
    try:
        docs =  await jsonfs.load_docs(name)
        max_doc = max(docs, key=lambda doc: doc["fieldname"])
        return datetime.fromisoformat(max_doc["createdDateTime"])
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(e)
        return datetime(1900, 1, 1)