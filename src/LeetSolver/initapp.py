# this is init function for the leetsolever the purpose of this function is to
# 1. search for the obb folder 
#     - 1st check in /home/{user-name}/.leetsolver
#     - 2nd look in currect directory
# 2. if not find in any place its create in /home/{user-name}/.leetsolver
# 3. if find in any place its return the path of the folder
# 4. check if the folder is empty or not
# 5. if empty create the default file in the folder
# 6. if not empty check if the file is correct or not
# 7. if not correct create the default file in the folder
# 8. if correct return the databse obeject

from LeetSolver.validators import (
    validate_sqlite_database,
    validate_json_file
)
from LeetSolver.error import (
    LeetSolverError,
    FolderValidationError
)
from LeetSolver.utils import IsPathReadAndWritable
from typing import Optional
from pathlib import Path


# scema and constants and data
__DIR_NAME = ".leetsolver"

__DIR_LIST = [
    Path("~").expanduser().resolve(),
    Path(__file__).resolve().parents[2]
]

__DEFULT_SETTINGS = {
    "logoid" : 0,
}

# make sure scmea is currect degined else riase error
__DEFAULT_SQLITE_SCHEMA = {
    "__version__": "v1",
    "__on_upgrade__": None,
    "Tables": [
        {
            "name": "questions",
            "columns": (
                (0, 'question_id', 'TEXT', 1, None, 1),
                (1, 'name', 'TEXT', 1, None, 0),
                (2, 'difficulty', 'TEXT', 0, None, 0, "CHECK(difficulty IN ('Easy', 'Medium', 'Hard'))"),
                (3, 'first_solved', 'DATE', 0, None, 0),
                (4, 'last_solved', 'DATE', 0, None, 0),
                (5, 'total_solved', 'INTEGER', 0, '0', 0),
                (6, 'personal_rating', 'INTEGER', 0, None, 0, "CHECK(personal_rating BETWEEN 1 AND 10)"),
                (7, 'best_rating', 'INTEGER', 0, None, 0),
                (8, 'current_rating', 'INTEGER', 0, None, 0),
                (9, 'magic_score', 'REAL', 0, None, 0),
                (10, 'tags', 'TEXT', 0, None, 0),
                (11, 'notes', 'TEXT', 0, None, 0)
            ),
            "constraints": {
                "FOREIGN KEY": [],
                "UNIQUE": []
            },
            "outer_statement": None
        },
        {
            "name": "daily_log",
            "columns":(
                (0, 'id', 'INTEGER', 1, None, 1, "AUTOINCREMENT"),
                (1, 'date', 'DATE', 1, None, 0),
                (2, 'question_id', 'TEXT', 1, None, 0),
                (3, 'time_taken', 'INTEGER', 0, None, 0),
                (4, 'success', 'BOOLEAN', 0, None, 0),
                (5, 'revision_status', 'BOOLEAN', 0, None, 0)
            ),
            "constraints": {
                "FOREIGN KEY": [
                    "FOREIGN KEY(question_id) REFERENCES questions(question_id)"
                ],
                "UNIQUE": []
            },
            "outer_statement": None
        },
        {
            "name": "weekly_summary",
            "columns": (
                (0, 'week_start', 'DATE', 1, None, 1, "PRIMARY KEY"),
                (1, 'total_questions', 'INTEGER', 0, None, 0),
                (2, 'easy_count', 'INTEGER', 0, None, 0),
                (3, 'medium_count', 'INTEGER', 0, None, 0),
                (4, 'hard_count', 'INTEGER', 0, None, 0)
            ),
            "constraints": {
                "FOREIGN KEY": [],
                "UNIQUE": []
            },
            "outer_statement": None
        }
        
    ],
    "Triggers": { },
    "Indexes": { },
}

__REQUIRED_FILES = [
    {
        "name": "settings.json",
        "schema": __DEFULT_SETTINGS,
        "validate": validate_json_file
    },
    {
        "name": "database.db",
        "schema": __DEFAULT_SQLITE_SCHEMA,
        "validate": validate_sqlite_database
    }
]


# main code
class Database:
    def __init__(self, path: Path):
        self.path = path

def get_dirpath() -> Optional[Path]:
    """
    Get or create the LeetSolver directory path.

    1. If an existing path is found and is writable, return it.
    2. Otherwise, try to create it in one of the base directories.
    3. Return None if all attempts fail.
    """
    for base_dir in __DIR_LIST:
        path = Path(base_dir) / __DIR_NAME
        if path.exists() and IsPathReadAndWritable(path):
            return path  

    for base_dir in __DIR_LIST:
        path = Path(base_dir) / __DIR_NAME
        try:
            path.mkdir(parents=True, exist_ok=True)
            return path
        except Exception:
            pass 
    
    return None

def validate_DIR(path: Path) -> None:
    """
    Validate the directory's required files.

    1. Loops through each file in the required file list.
    2. For each file, runs its associated validation method with the default schema and fix=True.
       - If the file is broken, the validation method tries to fix it silently.
       - If the file does not exist, it attempts to create it.
    3. If validation fails (e.g., unrecoverable error or file can't be fixed/created), 
       an exception is raised.
    4. This function catches those exceptions and raises a LeetSolverError instead.
    5. If the function completes without error, the directory is valid and ready to use.
    """
    for file in __REQUIRED_FILES:
        try:
            file['validate'](path / file['name'], schema=file['schema'], fix=True)
        except Exception as e:
            raise LeetSolverError(f"Initialization failed due to a technical error: {e}")

def init() -> Database:
    """
    Initialize the LeetSolver application.

    1. Locate or create the required directory for LeetSolver.
    2. Validate the directory and its required files.
    3. Return a Database object if initialization is successful.

    Raises:
        FolderValidationError: If the directory cannot be created or accessed.
        LeetSolverError: If directory validation fails.

    Returns:
        Database: A Database object initialized with the directory path.
    """
    path = get_dirpath()
    
    if path is None:
        raise FolderValidationError("[Error:001] Ensure the /home/user directory has write permissions.")
    
    validate_DIR(path)
    return Database(path)
