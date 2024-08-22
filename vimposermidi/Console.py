

class Console:
    """Hold messages to be send to the user."""
    lines: list[str]
    height: int

    def __init__(self, height: int) -> None:
        self.lines = []
        self.height = height

    def log(self, new_msg: str):
        if len(self.lines) == self.height:
            self.lines.pop(0)
        self.lines.append(new_msg)
