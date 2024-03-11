from itertools import groupby
from connectors.json_filesystem import JsonFilesystem

async def last_user_login_date(user_id:str, jsonfs: JsonFilesystem, name:str) -> str:
    "Last user login query"
    try:
        docs = await jsonfs.load_docs(name)
        docs_sorted = sorted(docs, key=lambda x: x["userId"])
        max_values = {}
        for key, group in groupby(docs_sorted, key=lambda x: x["userId"]):
            max_values[key] = max(group, key=lambda x: x["createdDateTime"])["createdDateTime"]
            
        if(user_id in max_values):
            return max_values[user_id]
        else:
            return "1900-01-01T00:00:00Z"   

    except Exception as e:
        print(f"Last User Login: ERROR {e}")
        return "1900-01-01T00:00:00Z"
        # return None
