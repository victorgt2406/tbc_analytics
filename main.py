import os
import importlib.util
from fastapi import FastAPI

app = FastAPI()


def load_routers(app, path='routes/', root='app'):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                # Generate the module name by the file path
                module_name = os.path.join(root, file).replace(
                    '/', '.').replace('\\', '.')
                module_name = module_name.replace('.py', '')

                # Load the module
                spec = importlib.util.spec_from_file_location(
                    module_name, os.path.join(root, file))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Register the router
                if hasattr(module, 'router'):
                    app.include_router(module.router, prefix='/'+module_name[len(
                        root)+1:].replace('.', '/').replace('/'+file[:-3], ''))


# Assuming your project structure starts in the 'app/api' directory
load_routers(app)
