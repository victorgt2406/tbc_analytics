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
    # async def upsert_docs(self, docs: List[Dict[str, Any]], name: str, id_key="id"):
    #     filepath = f"{self.directory}/{name}.{self.file_extension}"
    #     len_docs = len(docs)
    #     async with aiofiles.open(filepath, 'a') as file:
    #         for i, doc in enumerate(docs):
    #             await file.write(json.dumps(doc) + "\n")
    #             if i % 100 == 0:
    #                 await asyncio.sleep(1)
    #                 print(f"JsonFileSystem: {i/100}/{len_docs/100} 100 docs where stored")
    #     print(f"JsonFileSystem: {len_docs} where successfully stored")
    def set_up(self):
        self.conf:dict[str, Any] = load_config().get("json_filesystem", {})
        self.path = self.conf.get("path", "./archived")
        self.file_extension = self.conf.get("file_extension", "datajson")
    
    async def save_data(self, data: List[Dict[str, Any]], place: str, **args) -> None:
        await self.upsert_docs(data, place, id_key=args.get("id_key", "id"))

    async def upsert_docs(self, docs: List[Dict[str, Any]], filename: str, id_key="id"):
        "Save the docs in a file to the path selected"
        filename = f"{self.path}/{filename}.{self.file_extension}"

        existing_docs = await self.load_docs(filename)
        existing_docs_dict = {doc[id_key]: doc for doc in existing_docs}

        for doc in docs:
            doc_id = doc[id_key]
            existing_docs_dict[doc_id] = doc
        merged_docs = list(existing_docs_dict.values())
        async with aiofiles.open(filename, 'w') as file:
            for doc in merged_docs:
                await file.write(json.dumps(doc) + "\n")
        print(f"JsonFileSystem: {filename} was upgraded")

    async def load_docs(self, filename: str, start: int = 0, end: int = -1) -> List[Dict[str, Any]]:
        "Load the docs from a file"
        filepath = f"{self.path}/{filename}.{self.file_extension}"
        docs: List[Dict[str, Any]] = []
        current_index = 0
        end_index_adjusted = end - 1
        try:
            async with aiofiles.open(filepath, 'r') as file:
                async for line in file:
                    if current_index >= start and (end == -1 or current_index <= end_index_adjusted):
                        docs.append(json.loads(line))
                    current_index += 1
            return docs
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"JsonFileSystem: ERROR. When loading jsons JsonFileSystem {e}")
            return []
        
    async def convert_json_to_datajson(self, source_filename: str, name: str):
        """
        Converts a standard JSON file to a 'datajson' file format used by this class.

        - source_filename: Path to the source JSON file.
        - name: Name for the target 'datajson' file, without extension.
        """
        source_filepath = source_filename
        target_filepath = f"{self.path}/{name}.{self.file_extension}"

        # Read the entire JSON object/array from the source file
        async with aiofiles.open(source_filepath, 'r') as file:
            content = await file.read()
            data = json.loads(content)

        # Ensure the data is a list for consistency
        if not isinstance(data, list):
            data = [data]

        # Write each item in the list to the target file, one item per line
        async with aiofiles.open(target_filepath, 'w') as file:
            for item in data:
                await file.write(json.dumps(item) + "\n")

        print(f"Conversion complete: '{source_filepath}' to '{target_filepath}'") 
