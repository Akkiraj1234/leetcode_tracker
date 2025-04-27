from pathlib import Path
import os


def ISpathreadandwritable(path: Path) -> bool:
    return os.access(path, os.W_OK | os.R_OK)

def ISversioncompatible(current_version: str, required_version: str) -> bool:
    return tuple(map(int, current_version.split("."))
    ) >= tuple(map(int, required_version.split(".")))
    