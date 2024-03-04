from elasticsearch import Elasticsearch

def last_user_login_date(user_id:str, es: Elasticsearch, index) -> str:
    "Last user login query"
    try:
        res = es.search(
            index=index,
            query={
                "match": {
                    "userId": user_id
                }},
            sort=[
                {
                    "@timestamp": {
                        "order": "desc"
                    }
                }
            ],
            size=1
        )
        if(res["hits"]["total"]["value"]>0):
            return res["hits"]["hits"][0]["_source"]["@timestamp"]
        else:
            # print("total value" ,res["hits"]["total"]["value"])
            return "1900-01-01T00:00:00Z"
            # return None

    except Exception as e:
        print(f"Last User Login: ERROR {e}")
        return "1900-01-01T00:00:00Z"
        # return None
