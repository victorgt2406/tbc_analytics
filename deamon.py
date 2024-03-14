import asyncio
import os
from importlib import import_module
from bridges import Bridge
from utils.config import load_config
# from connectors.elk_msgraph import ElkMsgraph

# em = ElkMsgraph()
config: dict = load_config()
c_bridges: dict = config.get("bridges", {})
# c_bridges_exception:list = c_bridges.get("exceptions",["device_apps_bridge"])


def load_bridges() -> list[Bridge]:
    """
    Loads all the modules of the bridges inside `/deamon_bridges` directory

    ### Exception
    - It ignores the `/bridges/__init__.py` file
    - It ignores the bridges exceptions saved at /config.json
    """

    bridges: list[Bridge] = []
    path = "./deamon_bridges"
    files: list[str] = list(map(lambda x: f"{path}/{x}", os.listdir(path)))
    # bridges_exception_path = list(
    #     map(lambda x: f"{path}/{x}.py", c_bridges_exception))
    # files = list(filter(lambda file: file.endswith(".py") and not file.endswith(
    #     "__init__.py") and not file in bridges_exception_path, files))
    files = list(filter(lambda file: file.endswith(".py") and not file.endswith(
        "__init__.py"), files))
    print(files)
    for file in files:
        route_name = file.split("/")[-1][:-3]
        print(route_name)
        module_path = file[2:-3].replace("/", ".")
        print(module_path)
        module = import_module(module_path)
        bridges.append(module.bridge)
    return bridges


async def deamon():
    "Loads all the bridges to an infinit loop"
    bridges = load_bridges()
    await asyncio.gather(*(bridge.automatic_mode() for bridge in bridges))

asyncio.run(deamon())
