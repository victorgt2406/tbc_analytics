"""ELK abstraction"""

import os
from typing import List
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

from ms_graph import Msgraph

class ELK:
    """
    A class that abstract Elasticsearch to be used with msgraph easierly

    Attributes:
        `es`: Client of Elasticsearch.
    Methods:
        `to_esdocs`,
        `bulk_docs`

    """
    def __init__(self) -> None:
        self.setup_connections()
        self.ms_graph = Msgraph()

    def setup_connections(self):
        """
        Connect Elasticsearch ELK and sets the es connection
        """
        load_dotenv()
        cloud = os.getenv("ES_CLOUD")
        api_key = os.getenv("ES_API_KEY")

        self.es = Elasticsearch(cloud, api_key=api_key)

    def to_esdocs(self, docs:List[dict], index, id_key="id") -> List[dict]:
        """
        Transform a list of documents to a list ready to be bulk at Elasticsearch
        """
        docs_es = []
        for doc in docs:
            docs_es.append({"index": { "_index": index, "_id": doc[id_key]}})
            del doc["id"]
            docs_es.append(doc)
        return docs_es

    def bulk_docs(self, docs:List[dict], index, id_key="id"):
        """
        Buks the documents to Elasticsearch
        """
        docs_es = self.to_esdocs(docs, index, id_key)
        self.es.bulk(operations=docs_es)

    async def update_ms_graph(self):
        await self.ms_graph.async_init()
        self.bulk_docs(self.ms_graph.users, "users")
        self.bulk_docs(self.ms_graph.mobile_apps, "mobile_apps")
        self.bulk_docs(self.ms_graph.devices, "devices")