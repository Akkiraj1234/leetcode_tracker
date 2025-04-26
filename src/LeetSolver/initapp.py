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

from LeetSolver.utils import (
    validate_json_file,
    validate_database
)
from LeetSolver.error import (
    LeetSolverError,
    FolderValidationError
)
from typing import Optional
from pathlib import Path
import os


__DIR_LIST = [
    os.path.abspath(os.path.expanduser("~")),
    os.path.dirname(os.path.abspath(__file__))
]
__DIR_NAME = ".leetsolver"
__DEFULT_SETTINGS = {
    "logoid" : 0
}
__DEFULT_SQLITE_SCEMA = {
    "questions": {
        "question_id": "TEXT PRIMARY KEY",
        "name": "TEXT NOT NULL"
        ""
    }
}
__REQUIRED_FILES:list[dict[str:str,str:dict,str:callable]] = [
    {"name": "settings.json", "schema": __DEFULT_SETTINGS, "validate": validate_json_file},
    {"name": "database.db", "schema": __DEFULT_SQLITE_SCEMA, "validate": validate_database},
    # {"name": "pyui_extenstiones", "schema": None, "validate": validate_pyfolder},    #will work on future
    # {"name": "pyicons", "schema": None, "validate": validate_pyfolder}               #will work on future
]


class Database:
    def __init__(self, path: Path):
        self.path = path
        # self.connection = sqlite3.connect(path)
        # self.cursor = self.connection.cursor()

def get_dirpath() -> Optional[Path]:
    """
    Get or create the LeetSolver directory path.

    1. If an existing path is found and is writable, return it.
    2. Else, try to create it in one of the base dirs.
    3. Return None if all fail.
    """
    for base_dir in __DIR_LIST:
        path = Path(base_dir) / __DIR_NAME
        if path.exists() and os.access(path, os.W_OK):
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
    5. If the function completes without error, the directory is valid and ready.
    """
    for file in __REQUIRED_FILES:
        try:
            file['validate'](path / file['name'], schema=file['schema'], fix=True)
        except Exception as e:
            raise LeetSolverError(f"Initialization failed due to a technical error: {e}")

def init() -> None:
    path = get_dirpath()
    
    if path is None:
        raise FolderValidationError("[Error:001] make sure /home/user dir have writing permmison")
    
    validate_DIR(path)
    return Database(path)


# __DEFULT_BANNNER = {
#     "name": "defult-bot",
#     "size": (7, 5),
#     "frame-rate": 2,
#     "frame": [
#         [
#             (" ╭───╮ ", " ◉ ◉ | ", " ╰───╯ ", "   │   ", "   o   "),
#             (" ╭───╮ ", " - - | ", " ╰───╯ ", "   │   ", "   o   ")
#         ]
#     ]
# }