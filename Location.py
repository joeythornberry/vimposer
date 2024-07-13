class Location:
    """Hold a pair of (p, x) coords."""
    p: int
    x: int

    def __init__(self, p: int, x: int):
        """Init a Location with the specified coords."""
        self.p = p
        self.x = x
