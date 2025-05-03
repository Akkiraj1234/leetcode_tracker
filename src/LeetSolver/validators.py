from LeetSolver.utils import (
    IsPathReadAndWritable,
    IsPathExistAndUsable,
    IsVersionCompatible
)
from LeetSolver.error import (
    ValidationError, 
    PermissionErrorLS
)
from typing import Dict, Optional, Tuple
from pathlib import Path 
import sqlite3
import json

# Summary of Edge Cases and Actions for json data validation:
# [done] if not exists and invalid create new file
# [done] Missing keys are added with schema defaults.
# [done] Type mismatches are corrected by replacing the value with the schema’s value.
# [done] Nested dictionaries are recursively validated.
# [done] Invalid JSON and file-not-found errors are handled with empty dict.
# [done] Writes the modified JSON back to the file if fix=True.
# [done] File permissions check for read/write access.
# [not yet] Type conversion for mismatched types if possible (e.g., string to integer).
# [not yet] trying to fix broken json data with regeex
# [not yet] Logging modifications made during validation.
# [not yet] Performance optimizations for large files.
# [not yet] modifay misisng data from backup if possible

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
    if not IsPathExistAndUsable(json_fp):
        raise PermissionErrorLS(json_fp, "read and write")
    
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
# [done] if not exists and fix=false raise else database Corrupted create new file 
# [done] File permissions check for read/write access.
# [done] sqlite3 verstion checking if less then raise validation error
# [done] if tables is missing create it with schema
# [----] if colume Corrupted create a new table.
# [----] if anything mismatched in sqlite3 create a new table.
# [not yet] create backup and estire from backup
# [not yet] data extractor to extract data from broken table
# [not yet] Handle databae locks with rety mechanisms.
# [not yet] Logging modifications made during validation.
# [not yet] Implement a proper database migration strategy if sceema change
# ===========================================================================
# [SCHEMA DESIGN EXPLANATION]
# ===========================================================================
# 1. The dictionary-based schema design will be used for validation purposes
#    to ensure that the SQLite3 database structure follows the correct schema.
#    Note: This schema design will not include any built-in validation methods.
#    It assumes that the schema provided is always correct.
# 
# 2. The validation method will not perform direct modifications (e.g., ALTER) on 
#    the database tables. Instead, if any errors, corruption, or discrepancies 
#    are detected in the schema, the existing tables will be replaced with new ones. 
#    Why is this approach chosen?
#       - SQLite3 has limitations when it comes to altering tables.
#       - SQLite can only rename columns, add columns at the end of the table, 
#         and drop columns that aren't part of primary keys or unique constraints.
#       - As a result, it's often easier and cleaner to recreate the tables 
#         entirely rather than modifying them directly.
# 
# 3. The initial version (v1) of the schema design will not support views or 
#    virtual tables. These features may be considered in later versions, but 
#    they will not be included in the current implementation.
# ===========================================================================
# [SCHEMA DESIGN]
# ===========================================================================
# __DEMO_SQLITE_SCHEMA = {
#     "__version__": "v1",  # optional versioning for future upgrades
#     "__on_upgrade__": None,  # strategy for schema version mismatch should be callable(cursor,scema)
#     "Tables": [
#         {
#             "name": "demo",
#             "columns": [
#                 # (cid, name, type, notnull, default_value, pk, [optional] extra)
#                 (0, 'column1', 'TEXT', 1, None, 1),
#                 (1, 'column2', 'TEXT', 1, None, 0),
#                 (2, 'column3', 'TEXT', 0, "null", 0, "CHECK(column3 IN ('Easy', 'Medium', 'Hard'))"),
#                 (3, 'column4', 'TEXT', 1, None, 0, "GENERATED ALWAYS AS (price + tax) STORED"),
#             ),
#             "constraints": {
#                 "FOREIGN KEY": [
#                     "FOREIGN KEY (user_id) REFERENCES users(id)"
#                 ],
#                 "UNIQUE": [
#                     "UNIQUE (column1, column2)"
#                 ]
#             },
#             "outer_statement": ""  # Use "WITHOUT ROWID" or other directives if needed
#         }
#     ],
#     "Triggers": {
#         "update_timestamp": (
#             "CREATE TRIGGER update_timestamp AFTER UPDATE ON users "
#             "BEGIN UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id; END;"
#         )
#     },
#     "Indexes": {
#         "idx_name": "CREATE INDEX idx_name ON table_name(column_name);",
#         "idx_unique_name": "CREATE UNIQUE INDEX idx_unique_name ON table_name(column_name);",
#         "idx_partial": "CREATE INDEX idx_partial ON table_name(column_name) WHERE column_name IS NOT NULL;",
#         "idx_lower_name": "CREATE INDEX idx_lower_name ON table_name(LOWER(column_name));"
#     }
# }
# ===========================================================================
__REQUIRED_VERSION = "3.35.0"


def build_sqlite_column_definition(column: Tuple) -> str:
    """
    Builds a single column definition string for an SQLite CREATE TABLE statement.
    """
    return (
        f'{column[1]} {column[2]} {"NOT NULL " if column[3] else ""}'
        f'{f"DEFAULT {column[4]} " if column[4] else ""}'
        f'{"PRIMARY KEY " if column[5] else ""}'
        f'{column[6] if len(column) > 6 else ""}'
    )

def create_sqlite_table_query(schema: Dict) -> str:
    """
    Generates a full SQLite CREATE TABLE SQL query from the provided schema.
    """
    column_definitions = [build_sqlite_column_definition(col) for col in schema["columns"]]
    constraints = schema["constraints"]["FOREIGN KEY"] + schema["constraints"]["UNIQUE"]
    all_definitions = ", ".join(column_definitions + constraints)
    return f"CREATE TABLE {schema['name']} ({all_definitions}) {schema["outer_statement"]};"

def create_sqlite_tables(connection: sqlite3.Connection, table_schema: Dict) -> None:
    """
    Creates all tables defined in the full schema dictionary.
    """
    cursor = connection.cursor()
    for table_schema in table_schema["Tables"]:
        try:
            cursor.execute(create_sqlite_table_query(table_schema))
        except sqlite3.DatabaseError as e:
            raise ValidationError("sqlite", e)
    connection.commit()

def sqlite_table_issue(cursor: sqlite3.Connection, table_schema: Dict) -> None:
    table_info = cursor.execute(f"PRAGMA table_info({table_schema["name"]});").fetchall()
    table_info_quary = cursor.execute(
        f'SELECT sql FROM sqlite_master WHERE type = "table" AND name = "{table_schema['name']}";'
    )

def validate_sqlite_tables(connection: sqlite3.Connection, issue, table_schema) -> None:
    pass

def validate_sqlite_database(sqlite3_fp: Path, schema: Optional[Dict] = None, **kw) -> None:
    """
    Validates the given SQLite3 database against a schema and optionally fixes it.

    If the database is corrupted or missing, it creates a new file if `fix=True`.
    Ensures that all tables, columns, and constraints in the schema exist in the database.
    Returns True if successful, raises ValidationError otherwise.
    the base dir shuld have read and write permison enable
    
    Args:
        sqlite3_fp (Path): Path to the SQLite3 database file.
        schema (Optional[Dict]): Schema definition for the database.
        **kw: Additional options (e.g., fix=True to apply fixes).

    Raises:
        ValidationError: If validation fails and `fix=False`.
        PermissionErrorLS
    """
    # check if database exists and have read and write permison or not
    if not sqlite3_fp.exists() and not kw.get("fix", False):
        raise ValidationError("sqlite3 database", "no sqlite3 database exists")
    
    if not IsPathReadAndWritable(sqlite3_fp):
        raise PermissionErrorLS(sqlite3_fp, "read and write")
    
    # databse validation prossess databse either be connected or created
    with sqlite3.connect(Path,timeout = 5) as conn:
        cursor = conn.cursor()
        if not IsVersionCompatible(cursor.execute("SELECT sqlite_version();").fetchone()[0], __REQUIRED_VERSION):
            raise ValidationError("sqlite3 database", f"the version of sqlite3 database is < {__REQUIRED_VERSION}")
        
        #if scmea is not given there is no point checing futher so return 
        if not schema:
            return
        
        tables_list = frozenset(row[0] for row in cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';").fetchall())
        
        # checking tables
        for table_schema in schema["Tables"].items():
            issue = sqlite_table_issue(cursor, table_schema)
            validate_sqlite_tables(cursor, issue, table_schema)
            
        # checking Triggers and Indexes and fixing it.
        conn.commit()










#     # Validate columns
#     cursor.execute(f"PRAGMA table_info({table_name});")
#     existing_columns = {col[1]: col[2] for col in cursor.fetchall()}  # {name: type}
#     for column_name, column_type in table_schema["columns"].items():
#         if column_name not in existing_columns:
#             if not kw.get("fix", False):
#                 raise ValidationError(
#                     f"Column '{column_name}' is missing in table '{table_name}'."
#                 )
#             # Add the missing column if fix=True
#             cursor.execute(
#                 f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};"
#             )
#         elif existing_columns[column_name] != column_type:
#             if not kw.get("fix", False):
#                 raise ValidationError(
#                     f"Column '{column_name}' in table '{table_name}' has a mismatched type."
#                 )
#             # Handle mismatched column types (optional: create new column and migrate data)
#             new_column_name = f"{column_name}_new"
#             cursor.execute(
#                 f"ALTER TABLE {table_name} ADD COLUMN {new_column_name} {column_type};"
#             )
#             cursor.execute(
#                 f"UPDATE {table_name} SET {new_column_name} = {column_name};"
#             )
#             # Drop and rename logic (if supported by SQLite)

#     # Validate constraints (foreign keys)
#     if "constraints" in table_schema:
#         for constraint in table_schema["constraints"]:
#             # SQLite does not provide a direct way to check constraints, so this is a placeholder
#             # You can implement additional logic to validate constraints if needed
#             pass
