import blessed

class Panel:
    def __init__(self, term, x, y, width, height, title="", full_border=False):
        self.term = term
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = ""
        self.full_border = full_border

    def draw(self):
        ... #figure out later




