from sys import prefix


class KeyboardManager:

    def __init__(self, after_action_hook, display_keys = lambda msg: msg):
        self.prefix = ""
        self.keys = ""
        self.maps = {}
        self.display_keys = display_keys
        self.after_action_hook = after_action_hook
        self.getch = None

    def clear(self):
        self.prefix = ""
        self.keys = ""

    def listen(self, getch):
        self.getch = getch
        while True:
            c = getch()

            if c == "Q":
                break

            if c in ['0','1','2','3','4','5','6','7','8','9'] and self.keys == "":
                self.prefix += c
            else:
                self.keys += c

            if c == "\x1b":
                self.clear()

            self.display_keys(self.prefix + self.keys)

            try:
                p = 1 if (self.prefix == "") else int(self.prefix)
                self.maps[self.keys](p)
                self.after_action_hook()
                self.keys = ""
                self.prefix = ""

            except KeyError:
                pass

            finally:
                self.display_keys(self.prefix + self.keys)

    def map(self, keypresses, function):

        if ("\x1b" in keypresses):
            raise TypeError("Cannot map escape key")
        if ("Q" in keypresses):
            raise TypeError("Cannot map Q (emergency quit key)")

        for (pattern, _) in self.maps.items():
            if (keypresses in pattern):
                message = "ERROR: Map unreachable: " + pattern + " is already mapped, but you're trying to map " + keypresses
                #raise TypeError(message)
            if (pattern in keypresses):
                message = "ERROR: Map unreachable: " + pattern + " is already mapped, so " + keypresses + " will never be reached"
                #raise TypeError(message) 

        self.maps[keypresses] = function

    
    def getSuffix(self, count = None):

        if self.getch is None:
            raise ValueError("getch must be set before calling getSuffix")

        keys = ""

        while True:
            c = self.getch()
            if c == '\x1b':
                self.clear()
                return None

            elif c == '\r':
                return keys

            keys += c

            if count is not None and len(keys) == count:
                return keys
        
