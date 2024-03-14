import os
from typing import Any, List, Dict
import json
import aiofiles
from connectors import Saver
from utils.config import load_config

class JsonFilesystem(Saver[Dict[str,Any], str]):
    """
    Json File systems.

    Read files from the system
    Write files to the system
    """
    def __init__(self) -> None:
        self.set_up()
        super().__init__("JsonFileSystem")

    def set_up(self):
        self.conf:dict[str, Any] = load_config().get("json_filesystem", {})
        self.path = self.conf.get("path", "./archived")
    
    async def save_data(self, data: List[Dict[str, Any]], place: str, **args) -> None:
        await self.upsert_docs(data, place, id_key=args.get("id_key", "id"))

    async def upsert_docs(self, docs: List[Dict[str, Any]], filename: str, id_key="id"):
        "Save the json docs in a file to the path selected"
        os.makedirs(self.path, exist_ok=True)  # Ensure the directory exists
        filepath = f"{self.path}/{filename}.json"

        existing_docs = await self.load_docs(filename)
        existing_docs_dict = {doc[id_key]: doc for doc in existing_docs}

        for doc in docs:
            doc_id = doc[id_key]
            existing_docs_dict[doc_id] = {**existing_docs_dict.get(doc_id,{}),**doc}
        
        merged_docs = list(existing_docs_dict.values())

        async with aiofiles.open(filepath, 'w') as file:
            await file.write(json.dumps(merged_docs))
            
        print(f"JsonFileSystem: {filepath} was upgraded")

    async def load_docs(self, filename: str, start: int = 0, end: int = -1) -> List[Dict[str, Any]]:
        "Load the json docs from a file"
        filepath = f"{self.path}/{filename}.json"
        docs: List[Dict[str, Any]] = []
        try:
            async with aiofiles.open(filepath, 'r') as file:
                content = await file.read()
                docs = json.loads(content)
            # Slice the documents if start and end are specified
            if end != -1:
                return docs[start:end]
            else:
                return docs[start:]

        except FileNotFoundError:
            print(f"JsonFileSystem: File not found - {filepath}. Returning empty list.")
            return []
