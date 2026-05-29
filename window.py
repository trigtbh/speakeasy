from typing import *
from blessed import Terminal
import time

from panel import Panel
class Window:
    def __init__(self):
        self.term = Terminal()
        self.panels: List[Panel] = []
        self.tps = 20
        self.redraw = True
        self.lastx, self.lasty = self.term.width, self.term.height

    def render(self):
        print(self.term.clear)
        corners = set()
        for panel in self.panels:
            for b in panel.borders():
                (x1, y1), (x2, y2) = b
                corners |= set(b)
                if x1 == x2:
                    for i in range(y1 + 1, y2):
                        print(self.term.move_xy(x1, i) + "│", end="")
                else:
                    for i in range(x1 + 1, x2):
                        print(self.term.move_xy(i, y1) + "─", end="")
            panel.render()
        for c in corners:
            print(self.term.move_xy(*c) + "█", end="")



        print("", end="", flush=True)

    def run(self):
        with self.term.cbreak(), self.term.mouse_enabled(), self.term.hidden_cursor():
            while True:
                time.sleep(1/self.tps)
                if self.lastx != self.term.width or self.lasty != self.term.height:
                    self.redraw = True


                if self.redraw:
                    self.render()
                    self.redraw = False



                self.lastx, self.lasty = self.term.width, self.term.height


w = Window()
w.panels.append(Panel(w.term, 0, 0, 0.5, 1, title="Panel 1"))
w.panels.append(Panel(w.term, 0.5, 0, 0.5, 1, title="Panel 2"))

w.run()