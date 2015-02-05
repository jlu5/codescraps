#!/usr/bin/env python
try:
    from Tkinter import *
    from ttk import *
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
from n2w import numToWords
from sys import exit as sysexit

if __name__ == "__main__":
    root = Tk()
    root.title("n2w")

    # Initialize our variables
    out = StringVar()
    valid = BooleanVar()
    valid.set(0)
    out.set("Enter a number to convert into words.")

    def _copytoclipboard(*args):
        if valid.get():
            root.clipboard_clear()
            root.clipboard_append(out.get())
            cb.config(text = "Copied!")

    def _wrap_n2w(*args):
        inp = str(entry.get())
        cb.config(text = "Copy to Clipboard")
        try:
            s = numToWords(inp)
            out.set(s)
        except ValueError as e:
            out.set("Error: %s" % e)
            valid.set(0)
        else:
            print("Input: %s; Output: %s" % (inp, s))
            valid.set(1)

    entry = Entry(root, width=50, justify=CENTER)
    entry.grid(column=0, row=0, padx=5, pady=5, columnspan=2, sticky=(N))
    out_display = Label(root, textvariable=out, wraplength=500,
                        justify=CENTER)
    out_display.grid(row=1, columnspan=2, padx=5, pady=5, sticky=(N))

    rb = Button(root, text="Calculate", command=_wrap_n2w)
    rb.grid(row=2, padx=5, pady=5, sticky=(S))
    cb = Button(root, text="Copy to Clipboard", command=_copytoclipboard)
    cb.grid(row=2, padx=5, pady=5, column=1, sticky=(S))

    root.bind('<Return>', _wrap_n2w)
    root.bind('<Escape>', sysexit)

    # Make the window widgets resize automatically
    for x in range(2):
        root.columnconfigure(x, weight=1)
        root.rowconfigure(x, weight=1)
    entry.focus()
    root.mainloop()