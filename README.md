# Project TBC Analytics

Project TBC Analytics is a system designed to fetch, transform, and store data using various connectors with a focus on MsGraph and Elasticsearch (ELK).

# Setup

To run this project, you will need to:

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Configure [`.env`](#env). with the necessary credentials for Elasticsearch and MsGraph. 
4. Update [`config.json`](#configjson) with specific parameters for each bridge.
5. Start the daemon: `python daemon.py`.

# Components

The project is structured into several components:

- **Bridges**: Core abstractions for connecting different data sources and destinations.
- **Connectors**: Implementations for fetching data from MsGraph and saving it into Elasticsearch or a JSON file system.
- **Daemon**: A service that runs the bridges continuously in an automatic mode.
- **Utils**: Helper modules such as configuration management.
- **.env and config.json**: Configuration files for setting up external service credentials and bridge parameters.

## Bridges

A bridge is an abstract class that sets up a data flow between a data source (fetcher) and a data destination (saver). This is done through an asynchronous loop that periodically fetches and saves data.

### Bridge Lifecycle

1. **Setup**: Initialize the fetcher and saver with proper credentials.
2. **Start**: Begin the automatic fetching and saving process.
3. **Update Data**: Abstract method for fetching and saving data — to be implemented by subclasses.
4. **Stop**: End the automatic process.

## Connectors

Connectors are abstractions for the actions of fetching (`Fetcher`) and saving (`Saver`) data.

- `Fetcher`: Fetches data from a source such as MsGraph.
- `Saver`: Saves data into a destination like Elasticsearch or a JSON file system.
- `FetcherSaver`: A combination of fetching and saving in a single connector.

## MsGraph Connector

The `Msgraph` class handles the fetching of data from Microsoft Graph API.

### Setup

1. Uses MSAL to acquire a bearer token for authenticating API requests.
2. Configures API request parameters from `config.json`.

### Fetching Data

- Queries Microsoft Graph API and handles pagination to fetch all available data.
- Manages rate-limiting with retries after a configured wait time.

## ELK Connector

The `Elk` class deals with saving data into Elasticsearch.

### Setup

- Establishes a connection to the Elasticsearch cluster using credentials from `.env`.

### Saving Data

- Transforms data into Elasticsearch bulk format.
- Performs bulk index operations, with batching based on a configured threshold.

## JsonFilesystem Connector

Handles the saving of data into the local filesystem in JSON format.

### Setup

- Configures filesystem paths from `config.json`.

### Saving Data

- Merges new data with existing files.
- Ensures atomic writes for data integrity.

## Daemon

The `daemon.py` script is responsible for continuously running bridges.

### Behavior

- Dynamically loads bridge modules.
- Runs bridges in an infinite loop unless stopped.

## Setup

To run this project, you will need to:

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Configure `.env` with the necessary credentials for Elasticsearch and MsGraph.
4. Update `config.json` with specific parameters for each bridge.
5. Start the daemon: `python daemon.py`.

## Configuration

The behavior of bridges and connectors is configured via `config.json`. The file structures bridge-specific parameters such as fetch intervals and error handling strategies.

### Important Configurations for the bridges

- `fail_sleep`: How long to sleep after a failed operation before retrying.
- `sleep`: How long to wait between successful fetch/save cycles.

## Lab

Test and investigations with the connectors.

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

# config.json
```json
{
    "bridges": {
        "fail_sleep": 0.2,
        "ms_users": {
            "sleep": 3600,
            "licenses": {
                "26124093-3d78-432b-b5dc-48bf992543d5": "threat_protection",
                "05e9a617-0261-4cee-bb44-138d3ef5d965": "E3",
                "e0dfc8b9-9531-4ec8-94b4-9fec23b05fc8": "x-account"
            }
        },
        ...
        "ms_device_apps": {
            "sleep": 3600,
            "device_fields": [
                "id",
                "deviceName",
                "userId",
                "userDisplayName",
                "emailAddress",
                "operatingSystem",
                "osVersion",
                "lastSyncDateTime"
            ]
        }
    },
    "ms_graph": {
        "sleep": 0.1,
        "toomanyrequest_sleep": 25,
        "timeout": 60,
        "url_slicing": 60
    },
    "elk": {
        "sleep": 0.8,
        "threshold": 1000
    },
    "json_filesystem": {
        "sleep": 0.8,
        "threshold": 1000,
        "path": "./archived"
    }
}

```

# Create a new bridge:

Follow instructions in [bridges/README.md](./bridges/README.md/#create-a-new-bridge-with-new-connectors)

# Contribution

Feel free to contribute to the project by submitting pull requests or issues. Please adhere to the project's code of conduct and contribution guidelines.

# License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE.txt) file for details.

---
Generated by Víctor Gutiérrez Tovar during the internship in Tabacalera SLU
