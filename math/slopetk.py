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

    main = Frame(root)
    main.grid(column=0, row=0, sticky=(N, W, E, S))
    for x in range(5):
        main.columnconfigure(x, pad=5,weight=1)
        main.rowconfigure(x, pad=5,weight=1)
    main.pack(fill=BOTH, expand=YES)

    # Oh god, there's got to be a better way to initialize this...
    x1, y1, x2, y2, out, extra = StringVar(), StringVar(), StringVar(), \
        StringVar(), StringVar(), StringVar()

    def _slopeWrapper(*args):
        vars = tuple(map(float, map(Entry.get, (x1_entry,y1_entry,x2_entry,y2_entry))))
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

    # And this too...
    x1_entry = Entry(main, width=7, textvariable=x1)
    Label(main, text="x1").grid(column=0, row=0)
    x1_entry.grid(column=0, row=1)

    y1_entry = Entry(main, width=7, textvariable=y1)
    Label(main, text="y1").grid(column=1, row=0)
    y1_entry.grid(column=1, row=1)

    x2_entry = Entry(main, width=7, textvariable=x2)
    Label(main, text="x2").grid(column=2, row=0)
    x2_entry.grid(column=2, row=1)

    y2_entry = Entry(main, width=7, textvariable=y2)
    Label(main, text="y2").grid(column=3, row=0)
    y2_entry.grid(column=3, row=1)

    Label(main, textvariable=out).grid(column=0, row=2, columnspan=4)
    Button(main, text="Calculate", command=_slopeWrapper).grid(column=2,
        row=3, columnspan=2)
    Label(main, textvariable=extra).grid(column=0, row=3, columnspan=2)

    # Pad the app so it doesn't look all squished
    for child in main.winfo_children():
        child.grid_configure(padx=5, pady=5)

    x1_entry.focus()
    root.bind('<Return>', _slopeWrapper)

    root.mainloop()
