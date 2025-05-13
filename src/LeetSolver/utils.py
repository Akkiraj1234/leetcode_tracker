from __future__ import annotations
from typing import (
    List,
    Dict,
    Tuple,
    Iterator,
    Optional,
    Any
)
from pathlib import Path
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

def analyis_logo_data(data:List[str]):
    return (
        [
            ("╭───╮                   ", "◉ ◉ |   leet solver     ", "╰───╯ Solve|Learn|Repeat", "  0                     "),
            ("╭───╮                   ", "- - |   leet solver     ", "╰───╯ Solve|Learn|Repeat", "  0                     ")
        ],
        [800, 200]
    )

class ListNode:
    def __init__(self, var:Any = None, next_node:Optional[ListNode] = None) -> None:
        self.var = var 
        self.next = next_node

class Animation:
    def __init__(self, ms_per_call:int, frames:List[str], timestamps:List[int]) -> None:
        self.mspc = ms_per_call
        self.head = self.__load_frames(frames, timestamps)
        self.current = self.head
        self.ctime = 0
    
    def __load_frames(self, frames:List[str], timestamps:List[int]) -> Optional[ListNode]:
        dummy = curr = ListNode()
        for data in zip(frames, timestamps):
            curr.next = ListNode(data)
            curr = curr.next
        return dummy.next
    
    def __iter__(self):
        return self
    
    def __next__(self) -> Optional[str]:
        
        if self.current is None:
            self.current = self.head
            self.ctime = 0

        self.ctime += self.mspc
        
        if self.ctime < self.current.var[1]:
            return None
        
        frame = self.current.var[0]
        self.ctime = 0
        self.current = self.current.next
        return frame