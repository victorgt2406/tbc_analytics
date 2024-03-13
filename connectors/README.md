# Connectors

This module introduces a flexible, scalable approach to data interaction, enabling both the fetching and saving of data across various platforms. It's designed to provide a seamless integration with external data sources like Elasticsearch (ELK) and Microsoft Graph API, facilitating the efficient transfer and manipulation of data.

# Installation and Setup

Before using this module, ensure you have the necessary dependencies installed:

- aiohttp
- elasticsearch
- msal
- python-dotenv

Also, set up your environment variables appropriately (for example, Elasticsearch cloud ID and API key, Microsoft client ID, secret, and tenant ID). Make sure you have the `/.env` in the main path

# Overview

The core of this module lies in its abstract base classes and concrete implementations that cater to different data sources. It employs modern Python features such as asynchronous programming, type hints, and the ABC (Abstract Base Class) module to ensure robustness and developer-friendly code.

## Key Components

- **Connector Base Class**: Acts as the foundation for any data interaction class, ensuring consistent initialization and setup procedures.
- **Fetcher and Saver Classes**: Define abstract methods for fetching data from a source and saving data to a destination, respectively. These are generic classes, allowing for flexibility in the type of data they handle.
- **FetcherSaver Class**: A composite class that inherits from both Fetcher and Saver, facilitating classes that need to perform both actions.
- **Elk Class**: Implements the Saver interface for Elasticsearch, handling data indexing and bulk operations with consideration for performance and efficiency.
- **Msgraph Class**: Implements the Fetcher interface for Microsoft Graph API, providing methods to query and retrieve data in an efficient manner.

## Highlights

- **Asynchronous Data Operations**: Both fetching and saving operations are designed to be asynchronous, allowing for non-blocking I/O operations that are crucial for performance in network-bound tasks.
- **Generic Type Support**: The use of Python's `Generic` and `TypeVar` ensures that the module can work with various data types, enhancing its versatility.
- **Environmental Configuration**: Integration with `dotenv` for environment variables and a configuration management system ensures that the module can be easily adapted to different runtime environments without code changes.
- **Error Handling and Logging**: Thoughtful error handling and logging throughout the module ensure that any issues during data operations are clearly reported, aiding in debugging and monitoring.

# Usage

To use this module, you'll need to subclass the appropriate base class (`Fetcher`, `Saver`, or `FetcherSaver`) depending on your requirements. Implement the abstract methods with logic specific to your data source or destination.

## Elasticsearch Example

For interacting with Elasticsearch, instantiate the `Elk` class and call `save_data` with your documents:

```python
elk = Elk()
await elk.save_data(data=docs, place="your_index")
```

## Microsoft Graph API Example

For fetching data from Microsoft Graph API, instantiate the `Msgraph` class and use `fetch_data`:

```python
mg = Msgraph()
data = await mg.fetch_data("https://graph.microsoft.com/v1.0/me/messages")
```