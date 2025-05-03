from pathlib import Path
import os


def IsPathReadAndWritable(path: Path) -> bool:
    return os.access(path, os.W_OK | os.R_OK)

def IsPathExistAndUsable(path: Path) -> bool:
    return path.exists and ( path.is_fifo() or path.is_dir()
    ) and os.access(path, os.W_OK | os.R_OK)

def IsVersionCompatible(current_version: str, required_version: str) -> bool:
    return tuple(map(int, current_version.split("."))
    ) >= tuple(map(int, required_version.split(".")))
    