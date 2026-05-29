from blessed import Terminal
import curses


term = Terminal()

print(term.clear, flush=True)

with term.cbreak(), term.mouse_enabled(), term.hidden_cursor():
    while True:
        inp = term.inkey()
        if inp.name and inp.name.startswith('MOUSE_'):
            # print(inp.mouse_yx)
            # print(dir(inp))
            y, x = inp.mouse_yx
            # print(f"button {inp.name} at (y={y}, x={x})")
            print(term.move_yx(y, x) + term.on_color_hex('#ff5733')(" ") + term.normal, end="")
