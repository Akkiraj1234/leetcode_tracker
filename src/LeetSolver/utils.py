from LeetSolver.error import ValidationError
from typing import TextIO, LIST, Dict, Optional
from pathlib import Path
import json

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
            
    except json.JSONDecodeError as e:
        if not kw.get("fix", False):
            raise ValidationError(f"JSON decoding failed for '{json_fp}'. Error: {e}")
        json_data = {}

    # `validate_json_data` validates json data and fix data if necessary.
    #  and validate_json_data Returns True if the data was modified, False otherwise.
    if kw.get("fix", False) and schema and validate_json_data(json_data, schema): 
        with open(json_fp, 'w', encoding="utf-8") as file: 
            json.dump(json_data, file, indent=4)
    
def validate_database(database_fp: TextIO, tabes_scema: LIST[Dict[str:Dict]]) -> bool:
    """
    Validate a SQLite database file against a schema.

    Args:
        database_fp (TextIO): A file-like object containing the SQLite database.
        tabes_scema (list): A list of dictionaries representing the schema to validate against.

    Returns:
        bool: True if the database is valid according to the schema, False otherwise.
    """
    import sqlite3

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_fp)
        cursor = conn.cursor()
        
        # Iterate over the schema and validate each table
        for table_schema in tabes_scema:
            table_name = table_schema['name']
            columns = table_schema['columns']
            
            # Get the actual columns from the database
            cursor.execute(f"PRAGMA table_info({table_name})")
            actual_columns = cursor.fetchall()
            
            # Validate the columns
            for column in columns:
                if column not in [col[1] for col in actual_columns]:
                    return False
        
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()
    
def validate_pyfolder(folder_path: Path) -> bool:
    """
    Validate a folder to check if it contains Python files.

    Args:
        folder_path (str): The path to the folder to validate.

    Returns:
        bool: True if the folder contains Python files, False otherwise.
    """
    import os
    folder_path.mkdir(parents=True,exist_ok=True)
    folders = os.listdir(folder_path)
    (folder_path / "__init__.py").touch(exist_ok=True)
