class Note:
    l : int
    def __init__(self, l : int):
        self.l = l

    def __repr__(self):
        return f"<duration: {self.l}>"

