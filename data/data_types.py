from typing import List, Tuple, Set, Dict, Callable, Literal, Any
from tkinter import Event, Image as TkImage
from PIL.Image import Image as PILImage

from abc import abstractmethod

class TPlaylist():
    @abstractmethod
    def exists(self, id:int) -> bool: pass
    @abstractmethod
    def isListed(self, id:int) -> bool: pass
    @abstractmethod
    def items(self) -> Tuple[int,...]: pass
    @abstractmethod
    def firstItemVisible(self) -> int: pass
    @abstractmethod
    def next(self, id:int) -> int: pass