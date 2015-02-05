#!/usr/bin/env python

try:
    from Tkinter import *
    from ttk import *
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
from sys import exit as sysexit
import random

if __name__ == "__main__":
    root = Tk()
    root.title("some random button thingy")
    global buttons, maxsize
    maxsize = random.randint(3, 15)
    buttons = []

    def _createButton(*args):
        b = Button(root, text="OK", command=_createButton)
        buttons.append(b)
        _moveButton()

    def _moveButton(*args):
        global buttons
        if not buttons:
            _createButton()
        print(buttons)
        for b in buttons:
            r, c = [random.randint(0, maxsize) for _ in range(2)]
            b.grid(row=r, padx=5, pady=5, column=c)
    _moveButton()
    root.minsize(width=200, height=200)
    root.bind('<Enter>', _moveButton)
    root.bind('<Return>', _createButton)
    root.bind('<Escape>', sysexit)
    root.mainloop()
