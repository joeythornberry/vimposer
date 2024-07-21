from abc import ABC, ABCMeta, abstractmethod
from vimposermidi.Drawable import Drawable

class Frontend(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        """Set up everything the frontend needs to function, like the screen and such."""
        pass

    @abstractmethod
    def load_colors(self) -> int:
        """Do anything the frontend needs to set up colors, and return the total number of color ids."""
        return 0

    @abstractmethod
    def paint_ui_element(self, y: int, x: int, icon: str):
        """Paint the given UI icon to the given screen coordinates."""
        pass

    @abstractmethod
    def paint_pixel(self, d: Drawable):
        """Paint the given drawable to the screen."""
        pass

    @abstractmethod
    def close(self):
        """Tear down anything the frontend set up before closing it."""
        pass
