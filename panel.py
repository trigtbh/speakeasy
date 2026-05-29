import blessed
import time

class Panel:
    def __init__(self, term, x, y, width, height, title="", full_border=False):
        self.term = term
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = ""
        self.full_border = full_border

    def borders(self):
        width = self.term.width - 1
        height = self.term.height - 1

        borders = []
        if self.y != 0 or self.full_border:
            borders.append((
                (int(self.x * width), int(self.y * height)), 
                (int((self.x+self.width) * width), int(self.y * height))
            ))

        if self.x != 0 or self.full_border:
            borders.append((
                (int(self.x * width), int(self.y * height)), 
                (int(self.x * width), int((self.y+self.height) * height))
            ))

        if (self.y + self.height) != 1 or self.full_border:
            borders.append((
                (int(self.x * width), int((self.y+self.height) * height)), 
                (int((self.x+self.width) * width), int((self.y+self.height) * height))
            ))

        if (self.x + self.width) != 1 or self.full_border:
            borders.append((
                (int((self.x + self.width) * width), int(self.y * height)), 
                (int((self.x + self.width) * width), int((self.y+self.height) * height))
            ))

        return borders

term = blessed.Terminal()

p = Panel(term, 0, 0, 1, 0.2)
print(term.clear, flush=True)

if __name__ == "__main__":
    with term.cbreak(), term.mouse_enabled(), term.hidden_cursor():
        while True:
            print(term.clear)
            borders = p.borders()
            for b in borders:
                for point in b:
                    print(term.move_xy(*point) + "*", end="")
            print("", end="", flush=True)
            time.sleep(1/20)

