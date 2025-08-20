import json
from models.metadata_models import Metadata
from models.schema_models import Schema

def load_metadata_file(file_path: str) -> Metadata:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return Metadata(**data)

def load_schema_file(file_path: str) -> Schema:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return Schema(**data)