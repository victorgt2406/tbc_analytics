import asyncio
import os
from importlib import import_module
from bridges import Bridge
from connectors.elk_msgraph import ElkMsgraph

em = ElkMsgraph()

bridges_exception = ["device_apps_bridge"]


def load_bridges() -> list[Bridge]:
    """
    Loads all the bridges
    """

    bridges: list[Bridge] = []
    path = "./bridges"
    files: list[str] = list(map(lambda x: f"{path}/{x}", os.listdir(path)))
    bridges_exception_path = list(
        map(lambda x: f"{path}/{x}.py", bridges_exception))
    files = list(filter(lambda file: file.endswith(".py") and not file.endswith(
        "__init__.py") and not file in bridges_exception_path, files))
    print(files)
    for file in files:
        route_name = file.split("/")[-1][:-3]
        print(route_name)
        module_path = file[2:-3].replace("/", ".")
        print(module_path)
        module = import_module(module_path)
        bridges.append(module.bridge)
    return bridges


async def auto_update():
    bridges = load_bridges()
    await asyncio.gather(*(bridge.automatic_mode() for bridge in bridges))

    # await asyncio.gather(
    #     em.auto_update_basicdata(),
    #     em.auto_update_logins()
    # )

asyncio.run(auto_update())