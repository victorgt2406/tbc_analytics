# Bridge System Overview

The Bridge system is designed to facilitate data synchronization between different sources and destinations, specifically focusing on integrating Microsoft Graph API data with Elasticsearch. This system abstracts the fundamental operations required for fetching data from Microsoft Graph (via the `Msgraph` connector) and indexing it into Elasticsearch (via the `Elk` connector), providing a robust framework for extending functionality to various data types and sources.

# Core Components

## Abstract Bridge Class

- **File Location**: `bridges/__init__.py`

- **Purpose**: Serves as the base class for all bridge implementations. It defines a standard structure and workflow for data synchronization tasks, ensuring consistency and reusability across different bridge types.

- **Key Features**:
    - **Automatic and Manual Modes**: Bridges can operate in an automatic mode where data updates run indefinitely at specified intervals, or manually to execute a single update cycle.
    - **Extensibility**: The abstract method `update_data` allows subclasses to implement specific data fetching and processing logic.
    - **Configuration Loading**: Automatically loads and applies configuration settings specific to each bridge instance based on the `index` parameter, which corresponds to a section in the configuration file.
    - **Connectivity Setup**: Initializes connections to Elasticsearch and Microsoft Graph API, ensuring that data can be fetched and indexed effectively.

## BasicBridge Class

- **Purpose**: A extension of the `Bridge` abstract class that focuses on fetching data from predefined URLs (Microsoft Graph API endpoints) and indexing the responses into Elasticsearch.

- **Functionality**: Iterates over a list of URLs, queries data from Microsoft Graph API, and indexes the results into Elasticsearch. This class is tailored for straightforward scenarios where data fetching involves direct API requests without the need for extensive preprocessing.

# Usage Example

- **Bridge Instance**: `device_bridge.py` demonstrates how to instantiate and use a `BasicBridge` to synchronize data from Microsoft Graph API's managed devices endpoint into Elasticsearch.

- **Configuration**: The bridge system relies on a configuration file (`config.json`) that specifies operational parameters such as API endpoints, index names, and synchronization intervals.

## Getting Started

1. **Define URLs and Index**: Specify the Microsoft Graph API endpoints you wish to query and the Elasticsearch index where the data should be stored.

    ```python
    URLS = ["https://graph.microsoft.com/v1.0/deviceManagement/managedDevices"]
    INDEX = "ms_devices"
    ```

2. **Instantiate Bridge**: Create an instance of `BasicBridge` or another bridge subclass that matches your data synchronization needs.

    ```python
    bridge = BasicBridge(URLS, INDEX)
    ```

3. **Run Synchronization**: Choose between running the bridge in automatic mode for continuous updates or manually triggering a single update cycle.

    ```python
    # For automatic updates
    bridge.start()

    # For a single update cycle
    asyncio.run(bridge.run_once())
    ```

# Extending the Bridge System

To support new data sources or synchronization tasks, create a new subclass of `Bridge` and implement the `update_data` method with the desired logic. This design makes it easy to expand the system's capabilities while leveraging the existing framework for configuration management, connectivity setup, and operational modes.