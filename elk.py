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
        Connects to Elasticsearch cluster and updates the es client
        """
        load_dotenv()
        cloud = os.getenv("ES_CLOUD")
        api_key = os.getenv("ES_API_KEY")

        self.es = Elasticsearch(cloud, api_key=api_key)

    def to_esdocs(self, docs:List[dict], index, id_key="id") -> List[dict]:
        """
        This function transforms a list of documents, where each document is represented as a Python dictionary, into a format suitable for bulk operations in Elasticsearch.

        **Parameters:**

        - `docs: List[dict]`: A list of documents, where each document is a Python dictionary.
        - `index`: The Elasticsearch index where the documents will be stored.
        - `id_key="id"`: The key in each document dictionary that contains the document's ID. The default key is `"id"`.
        """
        docs_es = []
        for doc in docs:
            docs_es.append({"index": { "_index": index, "_id": doc[id_key]}})
            del doc["id"]
            docs_es.append(doc)
        return docs_es

    def bulk_docs(self, docs:List[dict], index, id_key="id"):
        """
        This function takes a list of documents and performs a bulk operation to insert them into an Elasticsearch index.

        ### Parameters:

        - `es: Elasticsearch`: An instance of the Elasticsearch client, used to interact with the Elasticsearch cluster.
        - `docs: List[dict]`: A list of documents, where each document is a Python dictionary.
        - `index`: The Elasticsearch index where the documents will be stored.
        - `id_key="id"`: The key in each document dictionary that contains the document's ID. The default key is `"id"`.
        """
        docs_es = self.to_esdocs(docs, index, id_key)
        self.es.bulk(operations=docs_es)

    async def update_ms_graph(self):
        """updates the basic values of ms_graph"""
        self.bulk_docs(await self.ms_graph.get_users(), "users")
        self.bulk_docs(await self.ms_graph.get_mobile_apps(), "mobile_apps")
        self.bulk_docs(await self.ms_graph.get_devices(), "devices")
        self.bulk_docs(await self.ms_graph.get_audit_logs(), "audit_logs")