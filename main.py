from importlib import import_module
import os
from fastapi import FastAPI
from elk import ELK

app = FastAPI()


def load_routes():
    versions = ["beta", "v1_0"]
    for version in versions:
        path = f"./routes/{version}"
        print(path)
        files:list[str] = list(map(lambda x: path+str(f"/{x}"),os.listdir(path)))
        files = list(filter(lambda x: x.endswith(".py"), files))
        print(files)
        for file in files:
            route_name = file.split("/")[-1][:-3]
            print(route_name)
            module_path = file[2:-3].replace("/", ".")
            print(module_path)
            module = import_module(module_path)
            app.include_router(module.router, prefix=f"/api/{version}/{route_name}")

load_routes()



if __name__ == "__main__":
    import asyncio
    elk = ELK()
    asyncio.run(elk.update_ms_graph())