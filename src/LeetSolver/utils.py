from pathlib import Path
import os


def ISpathreadandwritable(path: Path) -> bool:
    return os.access(path, os.W_OK | os.R_OK)