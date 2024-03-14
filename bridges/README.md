# Bridge

The Bridge component is a fundamental part of an asynchronous data processing system, designed to orchestrate the flow of data between various sources and destinations. It serves as a template for creating specific bridges that can fetch data using a Fetcher component, process or directly transfer it, and then save it using a Saver component. This document aims to provide a comprehensive guide to understanding, implementing, and utilizing the Bridge component effectively.

## Overview

A Bridge is an abstract class that outlines the necessary structure for data fetching and saving operations. It uses Generics to accommodate any type of Fetcher and Saver, making it highly versatile and applicable to a wide range of data sources and destinations. The Bridge's main responsibilities include initializing the Fetcher and Saver, managing their operations, and handling errors gracefully.

# Features

- **Generic Data Handling:** Supports any data source and destination by leveraging Fetcher and Saver components.
- **Asynchronous Operation:** Utilizes Python's asyncio for efficient non-blocking data processing.
- **Automatic and Manual Modes:** Capable of running continuous data processing cycles or a single cycle on demand.
- **Error Management:** Includes mechanisms for handling operational errors and implementing retry logic.

# Create a new bridge with new connectors

## Defining Fetcher and Saver Components

Implement Fetcher and Saver classes that inherit from their respective abstract bases. These components should define how data is fetched from a source and saved to a destination. For example:

```python
class MyFetcher(Fetcher):
    def set_up(self):
        # TODO
        pass
    async def fetch_data(self):
        # TODO
        pass

class MySaver(Saver):
    def set_up(self):
        # TODO
        pass
    async def save_data(self, data):
        # TODO
        pass
```

## Creating a Bridge Class

The Bridge component can be customized by overriding the `update_data` method in subclasses. This method defines the specific logic for how data should be processed between fetching and saving.

```python
class MyCustomBridge(Bridge[MyFetcher,MySaver]):
    def __init__(self, name: str) -> None:
        super().__init__(name, MyFetcher, MySaver)

    async def update_data(self):
        # Custom data processing logic
        pass
```

## Usage

### Running a Single Cycle

To execute a single fetch and save cycle:

```python
await my_bridge.run_once()
```

### Running automatically

To execute a single fetch and save cycle:

```python
await my_bridge.automatic_mode()
```

### Add it to the /deamon_bridges
```python
# deamon_bridges/my_custom_bridge.py
from where_ever_is_the_bridge import MyCustomBridge

bridge = MyCustomBridge("unnamed")
```


# Error Handling

Implement error handling within the `update_data` method or use the provided error handling mechanism to manage retries and failover strategies.