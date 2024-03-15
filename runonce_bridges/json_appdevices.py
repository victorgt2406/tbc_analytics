import asyncio
from deamon_bridges.json_deviceapps_bridge import bridge

asyncio.run(bridge.run_once())
