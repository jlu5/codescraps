#!/usr/bin/env python
try:
    from Tkinter import *
    from ttk import *
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
from factors import factors
from sys import exit as sysexit

if __name__ == "__main__":
    root = Tk()
    root.title("Factor Finder")
    Style().configure("TButton", padding=(3, 22, 3, 22))
    out = StringVar()

    def _factorsWrapper(*n):
        res = factors(entry.get())
        res = ', '.join(str(i) for i in res)
        out.set(res)

    entry = Entry(root, width=50, justify=CENTER)
    Label(root, text="Number:").grid(column=0, row=0, padx=5, pady=5, sticky=(S, N))
    entry.grid(column=1, row=0, padx=5, pady=5, sticky=(S, N, W, E))

    out_display = Label(root, textvariable=out, wraplength=500,
                        justify=CENTER, pad=10)
    out_display.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    Button(root, text="Calculate", command=_factorsWrapper).grid(column=0,
        row=2, columnspan=2, padx=5, pady=5, sticky=(W,E))

    entry.focus()
    root.bind('<Return>', _factorsWrapper)
    root.bind('<Escape>', sysexit)

    # Make the window widgets resize automatically
    for x in range(2):
        root.columnconfigure(x, weight=1)
        root.rowconfigure(x, weight=1)
    root.mainloop()
