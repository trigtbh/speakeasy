import blessed
import time
from abc import ABC, abstractmethod

from align import *
from tools import clean

class Drawable(ABC):
    @abstractmethod
    def __str__(self):
        return ""
    
    @abstractmethod
    def width(self) -> int:
        ...

    @abstractmethod
    def height(self) -> int:
        ...

class Text(Drawable):
    def __init__(self, string):
        self.string = string
        self.w = max(len(x) for x in string.split("\n"))
        self.h = len(string.split("\n"))

    def __str__(self):
        return self.string
    
    def width(self):
        return self.w
    
    def height(self):
        return self.h



class Panel:
    def __init__(self, term, x, y, width, height, title="", full_border=False):
        self.term = term
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.full_border = full_border

        self.top = self.y != 0 or self.full_border
        self.left = self.x != 0 or self.full_border
        self.right = (self.x + self.width) != 1 or self.full_border
        self.bottom = (self.y + self.height) != 1 or self.full_border

        self.drawable = (0, 0)
        if self.top and self.left:
            self.drawable = (1, 1)
        elif self.top:
            self.drawable = (0, 1)
        elif self.left:
            self.drawable = (1, 0)
    

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
    
    def _draw(self, item: Drawable, x: int | HorAlign, y: int | VertAlign):
        for i, line in enumerate(str(item).split("\n")):
            xp = 0
            w = int(self.term.width * self.width)
            truelen = len(clean(line))
            if x == HorAlign.LEFT:
                xp = 0
            elif x == HorAlign.CENTER:
                xp = w // 2 - truelen // 2
            elif x == HorAlign.RIGHT:
                xp = w - truelen
            else:
                xp = x

            yp = y
            h = int(self.term.height * self.height)
            if y == VertAlign.TOP:
                yp = i
            elif y == VertAlign.MIDDLE:
                yp = h // 2 - item.height() // 2 + i
            elif y == VertAlign.BOTTOM:
                yp = h - item.height() + i
            else:
                assert isinstance(y, int)
                yp = y + i

            if x == HorAlign.RIGHT and self.right:
                xp -= 1
            if x == HorAlign.LEFT and self.left:
                xp += 1
            if y == VertAlign.BOTTOM and self.bottom:
                yp -= 1
            if y == VertAlign.TOP and self.top:
                yp += 1


            xp += int(self.x * term.width)
            yp += int(self.y * term.height)

            print(self.term.move_xy(xp, yp) + line, end="")


    def render(self):
        if self.title: 
            self._draw(
                Text(self.title), HorAlign.CENTER, VertAlign.TOP
            )
        self._draw(Text("Hello\nWorld"), HorAlign.CENTER, VertAlign.MIDDLE)

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

