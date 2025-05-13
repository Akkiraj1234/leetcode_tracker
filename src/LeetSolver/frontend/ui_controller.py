from LeetSolver.frontend.ui_core import UICore
from LeetSolver.utils import (
    analyis_logo_data,
    Animation
)
from typing import List, Tuple, Optional, Iterator, Dict


class UIController:
    """
    """
    def __init__(self, ui_data:Dict, frame_repeat:int = 200):
        self.ui_data = ui_data
        self.frame_repeat = frame_repeat
        self.uic = UICore()
        
    def add_logo(self):
        frames, timestamps = analyis_logo_data(
            self.ui_data["logo_data"]
        )
        return Animation(self.frame_repeat, frames, timestamps)
    
    def setup(self):
        self.add_logo()
        
    def mainloop(self):
        pass