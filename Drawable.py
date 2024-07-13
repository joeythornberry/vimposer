from PixelData import PixelData

class Drawable:
    """Store all information the frontend needs to paint a (p, x) location.

    Attributes:
    icon -- What kind of thing is this pixel representing?
    icon_type -- Extra information that might influence how this pixel is drawn.
    cursor -- Is this pixel part of a cursored noted?
    color -- What color is this pixel?
    line, char -- The coordinates of the pixel.
    """
    
    icon: str
    icon_type: str
    cursor: bool
    color: int
    line: int
    char: int

    def __init__(self, pixel_data: PixelData):
        """Init a Drawable, using the cursor and icon values of the given PixelData"""
        self.cursor = pixel_data.cursor
        self.icon = pixel_data.icon

    def set_icon_type(self,new_icon: str):
        """Set the type value of the drawable."""
        self.icon_type = new_icon

    def set_cursor(self,is_cursor: bool):
        """Set the cursor value of the drawable."""
        self.cursor = is_cursor

    def set_color(self,new_color: int):
        """Set the color value of the drawable."""
        self.color = new_color

    def set_type(self,new_type: str):
        """Set the type value of the drawable."""
        self.type = new_type

    def set_line(self,new_line: int):
        """Set the line value of the drawable."""
        self.line = new_line

    def set_char(self,new_char: int):
        """Set the char value of the drawable. This is the coordinate, not the actual icon that is drawn (see Drawable.icon)."""
        self.char = new_char
