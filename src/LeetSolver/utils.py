from LeetSolver.error import ValidationError
from typing import TextIO, List, Dict, Optional
from pathlib import Path
import json
import os


def ISpathreadandwritable(path: Path) -> bool:
    return os.access(path, os.W_OK | os.R_OK)

def validate_json_data(json_data: Dict, schema: Dict) -> bool:
    modified = False
    
    for key, schema_value in schema.items():
        if key not in json_data:
            modified, json_data[key] = True, schema_value
            
        elif isinstance(schema_value, dict) and isinstance(json_data.get(key), dict):
            modified |= validate_json_data(json_data[key], schema_value)
            
        elif not isinstance(json_data[key], type(schema_value)):
            modified, json_data[key] = True, schema_value

    return modified


def validate_json_file(json_fp: Path, schema: Optional[Dict] = None, **kw) -> None:
    """
    Validates the given JSON file against a schema and optionally fixes it.
    Returns True if successful, raises ValidationError otherwise.
    """
    # check if json data is valid or not if yeah continue
    try:
        with open(json_fp, 'r', encoding="utf-8") as file: 
            json_data = json.load(file)
            
    except (json.JSONDecodeError, FileNotFoundError) as e:
        if not kw.get("fix", False):
            raise ValidationError(f"JSON decoding failed for '{json_fp}'. Error: {e}")
        json_data = {}

    # `validate_json_data` validates json data and fix data if necessary.
    #  and validate_json_data Returns True if the data was modified, False otherwise.
    if kw.get("fix", False) and schema and validate_json_data(json_data, schema): 
        with open(json_fp, 'w', encoding="utf-8") as file: 
            json.dump(json_data, file, indent=4)
    
