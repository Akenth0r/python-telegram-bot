from pathlib import Path
import json


# Save json string to file
def save_to_file(filepath: str, obj: dict):
    with open(filepath, 'w') as file:
        json.dump(obj, file, indent=4)


# Load json from file
def load_from_file(filepath: str):
    if not is_file_exist(filepath):
        return None
    with open(filepath, 'r') as file:
        return json.load(file)


def is_file_exist(filepath: str) -> bool:
    path = Path(filepath)
    if path.exists() and path.is_file():
        return True
    return False


def is_directory_exist(dirpath: str) -> bool:
    path = Path(dirpath)
    if path.exists() and path.is_dir():
        return True
    return False


