import sys
import asyncio
import os
from importlib import import_module


def load_bridges() -> list[str]:
    """
    Loads all the modules of the bridges inside `/deamon_bridges` directory

    ### Exception
    - It ignores the `/bridges/__init__.py` file
    - It ignores the bridges exceptions saved at /config.json
    """
    path = "./deamon_bridges"
    files: list[str] = list(map(lambda x: f"{path}/{x}", os.listdir(path)))
    files = list(filter(lambda file: file.endswith(".py"), files))
    return files




if len(sys.argv) > 1:
    # Print the first argument passed to the script
    bridge_path = sys.argv[1]
    bridge_paths = load_bridges()
    print(bridge_paths)
    print(sys.argv[1])
    if bridge_path in bridge_paths:
        module_path = bridge_path[2:-3].replace("/", ".")
        print(module_path)
        module = import_module(module_path)
        asyncio.run(module.bridge.run_once())
    else:
        print("deamon_bridge argument does not exist.")

else:
    print("No deamon_bridge argument was provided.")