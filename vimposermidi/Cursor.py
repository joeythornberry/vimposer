class Cursor:
    """Store the (p, x) coordinates of the cursored Note."""
    p: int
    x: int

    def __init__(self, p: int, x: int):
        """Init a new Cursor with the given coords."""
        self.p = p
        self.x = x

    def set(self, p: int, x: int): 
        """Set the Cursor's coords to the given values."""
        self.p = p
        self.x = x
