from datetime import datetime

from elasticsearch import Elasticsearch


def last_login_date(es:Elasticsearch) -> datetime:
    """
    Get the last login date
    """
    index = "logs-ms_singins"
    try:
        last_date = es.search(
            index=index,
            size=0,
            aggs={
                "latestDate": {
                    "max": {
                        "field": "createdDateTime"
                    }
                }
            }
        )["aggregations"]["latestDate"]["value_as_string"]
        return datetime.strptime(last_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(e)
        return datetime(2023, 11, 1)