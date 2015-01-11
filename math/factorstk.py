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

    main = Frame(root, relief=RAISED, borderwidth=1)
    main.pack(fill=BOTH, expand=YES)
    for x in range(2):
        main.columnconfigure(x, pad=5,weight=1)
        main.rowconfigure(x, pad=5,weight=1)
    Style().configure("TButton", padding=(3, 22, 3, 22))

    inp, out = IntVar(), StringVar()

    def _factorsWrapper(*n):
        res = factors(entry.get())
        res = ', '.join(str(i) for i in res)
        out.set(res)

    entry = Entry(main, width=50, textvariable=inp, justify=CENTER)
    Label(main, text="Number:").grid(column=0, row=0, sticky=(S, N))
    entry.grid(column=1, row=0, padx=5, pady=5, sticky=(S, N, W, E))

    Label(main, textvariable=out, wraplength=500, justify=CENTER, pad=10).grid(column=0,
        row=1, columnspan=2)
    Button(main, text="Calculate", command=_factorsWrapper).grid(column=0,
        row=2, columnspan=2, sticky=(W,E))

    entry.focus()
    root.bind('<Return>', _factorsWrapper)
    root.bind('<space>', lambda e: "break")
    root.bind('<Escape>', sysexit)

    root.mainloop()
