"""ELK abstraction"""

import asyncio
import os
from typing import List
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from utils.config import load_config


class Elk:
    """
    A class that abstract Elasticsearch

    Attributes:
        `es`: Client of Elasticsearch.
    Methods:
        `to_esdocs`,
        `bulk_docs`

    """

    def __init__(self) -> None:
        self.setup_connections()

    def setup_connections(self):
        """
        Connects to Elasticsearch cluster and updates the es client
        """
        load_dotenv()
        cloud = os.getenv("ES_CLOUD")
        api_key = os.getenv("ES_API_KEY")

        self.es = Elasticsearch(cloud, api_key=api_key)
        print("Elasticsearch: Connection sucessful")

    def to_esdocs(self, docs: List[dict], index, id_key="id") -> List[dict]:
        """
        This function transforms a list of documents, where each document is represented as a Python dictionary, into a format suitable for bulk operations in Elasticsearch.

        **Parameters:**

        - `docs: List[dict]`: A list of documents, where each document is a Python dictionary.
        - `index`: The Elasticsearch index where the documents will be stored.
        - `id_key="id"`: The key in each document dictionary that contains the document's ID. The default key is `"id"`.
        """
        docs_es = []
        for doc in docs:
            docs_es.append({
                "update": {
                    "_index": index,
                    "_id": doc[id_key]
                }
            })
            del doc[id_key]
            docs_es.append({
                "doc": doc,
                "doc_as_upsert": True
            })
        return docs_es

    async def bulk_docs(self, docs: List[dict], index, id_key="id"):
        """
        This function takes a list of documents and performs a bulk operation to insert them into an Elasticsearch index.

        ### Parameters:

        - `es: Elasticsearch`: An instance of the Elasticsearch client, used to interact with the Elasticsearch cluster.
        - `docs: List[dict]`: A list of documents, where each document is a Python dictionary.
        - `index`: The Elasticsearch index where the documents will be stored.
        - `id_key="id"`: The key in each document dictionary that contains the document's ID. The default key is `"id"`.
        """
        docs_es = self.to_esdocs(docs, index, id_key)
        print(f"Elasticsearch: {
              len(docs)} docs where transformed to be indexed at {index}")
        threshold = load_config().get("elk", {}).get("threshold", 500)
        if len(docs) > threshold:
            def divide_list(arr: list, n: int):
                return [arr[i:i + n] for i in range(0, len(arr), n)]

            lists_docs_es = divide_list(docs_es, threshold)
            len_lists = len(lists_docs_es)
            for i, list_docs_es in enumerate(lists_docs_es):
                res = self.es.bulk(operations=list_docs_es)
                await asyncio.sleep(0.5)
                if "errors" in res and res["errors"]:
                    break
                else:
                    print(f"Elasticsearch: ({
                          i+1}/{len_lists}) {len(list_docs_es)//2} docs where index at {index}")
        elif len(docs) > 0:
            res = self.es.bulk(operations=docs_es)
            print(f"Elasticsearch: (1/1) {len(docs)
                                          } docs where index at {index} ")
        print(f"Elasticsearch: {
                len(docs)} docs where succesfully indexed at {index}")
