from PixelData import PixelData

class Drawable:
    
    icon : str
    cursor : bool
    color : int
    type : str
    y : int
    x : int

    def __init__(self, pd : PixelData):
        self.cursor = pd.cursor
        self.icon = pd.icon

    def set_icon(self,i : str):
        self.icon = i

    def set_cursor(self,c : bool):
        self.cursor = c

    def set_color(self,c : int):
        self.color = c

    def set_type(self,t : str):
        self.type = t

    def set_y(self,y : int):
        self.y = y

    def set_x(self,x : int):
        self.x = x
