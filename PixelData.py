class PixelData:
    cursor : bool = False
    icon : str

    def set_icon(self, i : str):
        self.icon = i

    def set_cursor(self, c : bool):
        self.cursor = c
