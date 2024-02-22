"""ELK abstraction"""

import asyncio
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
        self.update = False

    def setup_connections(self):
        """
        Connects to Elasticsearch cluster and updates the es client
        """
        load_dotenv()
        cloud = os.getenv("ES_CLOUD")
        api_key = os.getenv("ES_API_KEY")

        self.es = Elasticsearch(cloud, api_key=api_key)
        print("Elasticsearch: Connection sucessful")

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

    async def bulk_docs(self, docs:List[dict], index, id_key="id"):
        """
        This function takes a list of documents and performs a bulk operation to insert them into an Elasticsearch index.

        ### Parameters:

        - `es: Elasticsearch`: An instance of the Elasticsearch client, used to interact with the Elasticsearch cluster.
        - `docs: List[dict]`: A list of documents, where each document is a Python dictionary.
        - `index`: The Elasticsearch index where the documents will be stored.
        - `id_key="id"`: The key in each document dictionary that contains the document's ID. The default key is `"id"`.
        """
        docs_es = self.to_esdocs(docs, index, id_key)
        print(f"Elasticsearch: {len(docs)} docs where transformed to be indexed")
        if len(docs) > 1000:
            def divide_list(arr:list, n:int):
                # Usar una comprensión de lista para generar los sub-arrays
                return [arr[i:i + n] for i in range(0, len(arr), n)]
            lists_docs_es = divide_list(docs_es, 500)
            len_lists = len(lists_docs_es)
            for i, list_docs_es in enumerate(lists_docs_es):
                res = self.es.bulk(operations=list_docs_es)
                print(res)
                await asyncio.sleep(0.5)
                print(f"Elasticsearch: {len(list_docs_es)} docs where index at {index} {i+1}/{len_lists}")
        else:
            res = self.es.bulk(operations=docs_es)
            print(f"Elasticsearch: {len(docs)} docs where index at {index} 1/1")

    async def update_ms_graph(self):
        """updates the basic values of ms_graph"""
        # await self.bulk_docs(await self.ms_graph.get_users(), "users")
        # await self.bulk_docs(await self.ms_graph.get_mobile_apps(), "mobile_apps")
        # await self.bulk_docs(await self.ms_graph.get_devices(), "devices")
        await self.bulk_docs(await self.ms_graph.get_auditlogs(), "logs-ms_auditlogs")

    async def auto_update_ms_graph(self):
        """Auto update ms graph data to elasticsearch"""
        print("Elasticsearch: Auto update ms_graph started")
        while True:
            await self.update_ms_graph()
            await asyncio.sleep(2*60)