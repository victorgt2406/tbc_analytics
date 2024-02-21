"""


By Víctor Gutiérrez Tovar
"""
from importlib import import_module
import asyncio
import os
from fastapi import FastAPI
from elk import ELK

app = FastAPI()


def load_routes():
    """
    Loads all the routes of the api
    """
    versions = ["beta", "v1_0"]
    for version in versions:
        path = f"./routes/{version}"
        print(path)
        files:list[str] = list(map(lambda x: f"{path}/{x}", os.listdir(path)))
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

@app.on_event("startup")
async def startup_event():
    """Función para ejecutar al iniciar la aplicación."""
    app.state.elk = ELK()
    # Asigna la tarea a un atributo del estado de la app si necesitas cancelarla luego.
    app.state.update_task = asyncio.create_task(app.state.elk.auto_update_ms_graph())

@app.on_event("shutdown")
async def shutdown_event():
    """Función para ejecutar al cerrar la aplicación."""
    print("Elasticsearch: Auto update ms_graph ended")
    app.state.update_task.cancel()
    try:
        await app.state.update_task
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
