# tbc_elk_analytics

Tabacalera Middleware API for Elastic Stack (Elk) working with Microsoft Graph API (MsGraoh)

# Requirements

-   Python 3.12
-   ELK server
-   MsGraph requirements

# Project organization

-   Bridges
-   Connectors
-   Lab
-   Queries
-   Routes
-   Utils

# Deamon `deamon.py`

-   The deamon imports all the `bridge` modules from the `/bridges` directory.
-   Each bridge handels it self to update its data automatically
-   It runs indefinetly

# Bridges

Classes that gets the data from MsGraph and sends that data to Elasticsearch cloud
Bridges classes extends the Bridge abstract class defined at `__init__.py`.

## Basic Bridge

This brige just gets all the data from a query of MsGraph and stores it in Elasticsearch cloud.

## Other bridges

These bridges are created customly so it updates the data more customly

# Lab

Where all the different queries from the bridges are tested to know the date they return.

-   MsGraph for all the msgraph queries
-   Elasticsearch for all the elastisearch queries

# .env

```bash
# Elasticsearch
ES_CLOUD="es_cloud"
ES_API_KEY="es_key"
# Microsoft
MS_CLIENT_ID="ms_client_id"
MS_CLIENT_SECRET="ms_secret_id"
MS_TENANT_ID="ms_tenant_id"
```
