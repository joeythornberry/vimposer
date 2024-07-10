class Cursor:
    p : int
    x : int

    def __init__(self,p,x):
        self.p = p
        self.x = x

    def set(self,p,x):
        self.p = p
        self.x = x
