"Load config.json"
import json

FILE_PATH = "./config.json"

def load_config() -> dict:
    "loads the config data"
    with open(FILE_PATH, 'r', encoding="utf-8") as file:
        return json.load(file)

def save_config(data: dict):
    "Saves the updated config"
    with open(FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)