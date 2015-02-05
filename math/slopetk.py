#!/usr/bin/env python
try:
    from Tkinter import *
    from ttk import *
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
from slope import *

if __name__ == "__main__":
    root = Tk()
    root.title("SlopeCalc!")

    # Make the window widgets resize automatically
    for x in range(4):
        root.columnconfigure(x, weight=1)
        root.rowconfigure(x, weight=1)

    out, extra = StringVar(), StringVar()
    _keys = ("x1", "y1", "x2", "y2")

    def _slopeWrapper(*args):
        global _keys
        vars = [numberwidgets[k] for k in _keys]
        vars = map(float, map(Entry.get, vars))
        vars = tuple(vars)
        if len(set(vars)) > 1:
            try:
                m = getslope(*vars)
                result = intercept(m, vars[0], vars[1])
                if vars[0] == vars[2]:
                    extra.set("Vertical Line!")
                elif vars[1] == vars[3]:
                    extra.set("Horizontal Line!")
                else:
                    extra.set("")
                out.set(result)
            except ValueError:
                pass

    # This dict allows us to declare our variables in a loop, saving
    # space and reducing code duplication
    numberwidgets = {}
    for nw in _keys:
        position = _keys.index(nw)
        numberwidgets[nw] = Entry(root, width=7)
        Label(root, text=nw).grid(column=position, row=0)
        numberwidgets[nw].grid(column=position, row=1)

    Label(root, textvariable=out).grid(column=0, row=2, columnspan=4)
    Button(root, text="Calculate", command=_slopeWrapper).grid(column=2,
        row=3, columnspan=2)
    Label(root, textvariable=extra).grid(column=0, row=3, columnspan=2)

    # Pad the app so it doesn't look all squished
    for child in root.winfo_children():
        child.grid_configure(padx=5, pady=5)

    numberwidgets['x1'].focus()
    root.bind('<Return>', _slopeWrapper)

    root.mainloop()
