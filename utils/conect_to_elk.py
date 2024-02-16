from dotenv import load_dotenv
import os
from elasticsearch import Elasticsearch
from msal import ConfidentialClientApplication
import requests

load_dotenv()

# Conexión elasticsearch
es_cloud = os.getenv("ES_CLOUD")
es_api_key = os.getenv("ES_API_KEY")

es = Elasticsearch(es_cloud, api_key=es_api_key)

es.info()

# Conexión con msgraph
ms_client_id = os.getenv("MS_CLIENT_ID")
ms_client_secret = os.getenv("MS_CLIENT_SECRET")
ms_tenant_id = os.getenv("MS_TENANT_ID")

ms_authority = f"https://login.microsoftonline.com/{ms_tenant_id}"
ms_scope = ["https://graph.microsoft.com/.default"]

ms = ConfidentialClientApplication(ms_client_id, authority=ms_authority, client_credential=ms_client_secret)

ms_token_res = ms.acquire_token_for_client(scopes=ms_scope)
ms_token:str = ms_token_res.get("access_token") # type: ignore
ms_headers = {'Authorization': f'Bearer {ms_token}'} # token microsoft

# URL de msgraph para obtener a los usuarios
graph_url = 'https://graph.microsoft.com/v1.0/users'

# Realizar la solicitud GET
response = requests.get(graph_url, headers=ms_headers)
docs = response.json()["value"]

docs_es = []
for doc in docs:
    docs_es.append({"index": { "_index": "ms_users", "_id": doc["id"]}})
    del doc["id"]
    docs_es.append(doc)

es.bulk(operations=docs_es)