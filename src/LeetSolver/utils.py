from pathlib import Path
from itertools import chain
import os


def IsPathReadAndWritable(path: Path) -> bool:
    return os.access(path, os.W_OK | os.R_OK)

def IsPathExistAndUsable(path: Path) -> bool:
    return path.exists() and ( path.is_file() or path.is_dir()
    ) and os.access(path, os.W_OK | os.R_OK)

def IsVersionCompatible(current_version: str, required_version: str) -> bool:
    return tuple(map(int, current_version.split("."))
    ) >= tuple(map(int, required_version.split(".")))
    
def remove_whitespace(test: str, lowercase: bool = True) -> str:
    """
    Removes all whitespace from the input string and optionally converts it to lowercase.
    """
    # Use generator expression for memory efficiency
    processed = ''.join(char for char in test if not char.isspace())
    return processed.lower() if lowercase else processed