from elasticsearch import Elasticsearch

def last_user_login_date(user_id:str, es: Elasticsearch, index) -> str:
    "Last user login query"
    try:
        res = es.search(
            index=index,
            query={
                "term": {
                    "userId.keyword": user_id
                }},
            sort=[
                {
                    "createdDateTime": {
                        "order": "desc"
                    }
                }
            ],
            size=1
        )
        if(user_id == "a3698c4e-1397-4f98-8046-452a8a42b28c"):
            print(res["hits"])
        if(res["hits"]["total"]["value"]>0):
            return res["hits"]["hits"][0]["_source"]["createdDateTime"]
        else:
            return "1900-01-01T00:00:00Z"

    except Exception as e:
        print(f"Last User Login: ERROR {e}")
        return "1900-01-01T00:00:00Z"
        # return None
