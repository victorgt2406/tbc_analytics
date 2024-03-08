import asyncio
from typing import Any, List, Dict
import json
import aiofiles

class JsonFilesystem:
    def __init__(self, directory="./archived", file_extension="datajson") -> None:
        self.directory = directory
        self.file_extension = file_extension

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


    async def upsert_docs(self, docs: List[Dict[str, Any]], name: str, id_key="id"):
        filepath = f"{self.directory}/{name}.{self.file_extension}"

        existing_docs = await self.load_docs(name)
        existing_docs_dict = {doc[id_key]: doc for doc in existing_docs}

        for doc in docs:
            doc_id = doc[id_key]
            existing_docs_dict[doc_id] = doc
        merged_docs = list(existing_docs_dict.values())
        async with aiofiles.open(filepath, 'w') as file:
            for doc in merged_docs:
                await file.write(json.dumps(doc) + "\n")
        print(f"JsonFileSystem: {name} was upgraded")

    async def load_docs(self, filename: str, start: int = 0, end: int = -1) -> List[Dict[str, Any]]:
        filepath = f"{self.directory}/{filename}.{self.file_extension}"
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
        except:
            return []
        
    async def convert_json_to_datajson(self, source_filename: str, name: str):
        """
        Converts a standard JSON file to a 'datajson' file format used by this class.

        - source_filename: Path to the source JSON file.
        - name: Name for the target 'datajson' file, without extension.
        """
        source_filepath = source_filename
        target_filepath = f"{self.directory}/{name}.{self.file_extension}"

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
