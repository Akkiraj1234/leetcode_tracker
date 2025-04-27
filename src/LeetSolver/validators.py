from LeetSolver.utils import ISpathreadandwritable
from LeetSolver.error import ValidationError
from typing import Dict, Optional
from pathlib import Path
import sqlite3
import json

# Summary of Edge Cases and Actions for json data validation:
# 1. [done] Missing keys are added with schema defaults.
# 2. [done] Type mismatches are corrected by replacing the value with the schema’s value.
# 3. [done] Nested dictionaries are recursively validated.
# 4. [done] Invalid JSON and file-not-found errors are handled with empty dict.
# 5. [done] Writes the modified JSON back to the file if fix=True.
# 7. [not yet] Type conversion for mismatched types if possible (e.g., string to integer).
# 8. [not yet] trying to fix broken json data with regeex
# 10. [not yet] Logging modifications made during validation.
# 11. [not yet] Performance optimizations for large files.
# 12. [not sure] File permissions check for read/write access.
# 13. [not yet] modifay misisng data from backup if possible

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

# Summary of Edge Cases and Actions for sqlite3 data validation:
# 1. Database Corruption: Catch errors and recreate the database
# 2. Permissions Issues: Check and adjust file permissions.
# 3. Database Size: Monitor the database size and implement size-limiting strategies.
# 4. Missing Tables: Recreate missing tables if necessary.
# 5. Missing Columns: Add missing columns, but be mindful of data types and potential inconsistencies.
# 6. Column Data Type Mismatch: Handle via migration or recreation of tables.
# 7. Foreign Key Issues: Ensure foreign keys are enabled and data consistency is maintained.
# 8. Constraint Violations: Validate data integrity and handle violations (either clean or report).
# 9. Database Locking: Handle database locks with retry mechanisms.
# 10. Inconsistent Foreign Keys: Check for orphaned foreign key references.
# 11. Schema Changes: Implement a proper database migration strategy.
# 12. SQLite Version Incompatibility: Ensure the SQLite version is compatible and migrate if necessary.
# 13. Missing Indexes: Validate and add missing indexes for performance.

def validate_sqlite_database(sqlite3_fp: Path, schema: Optional[Dict] = None, **kw) -> None:
    """
    validate the given sqlite3 database against a scema and optionally fixes it.
    return Trhe if succsessful, raises ValidationError otherwise.
    """
    for table in schema:
        
        pass

