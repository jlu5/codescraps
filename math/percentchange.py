#!/usr/bin/env python3
# The MIT License (MIT)

# Copyright (c) 2015,2017 James Lu

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

try:
    from Tkinter import *
    from ttk import *
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
from sys import exit as sysexit

def percentChange(a, b):
    """<a> <b>

    Find the percentage change between <a> and <b>."""
    return ((b - a) / a) * 100

if __name__ == "__main__":
    root = Tk()
    root.title("Percentage Change Calculator")

    out, env1, env2 = [StringVar() for _ in range(3)]

    def _wrap_percentChange(*args):
        try:
            a, b = map(float, (env1.get(), env2.get()))
            s = percentChange(a, b)
            out.set("%s%%" % s)
        except ZeroDivisionError:
            out.set("Initial value cannot be zero!")
        except (ValueError, ArithmeticError) as e:
            out.set("Error: %s" % e)

    def _swap(*args):
        a, b = env1.get(), env2.get()
        env1.set(b)
        env2.set(a)

    desc1 = Label(root, text="Initial value", justify=CENTER)
    desc2 = Label(root, text="Final value", justify=CENTER)
    desc1.grid(column=0, row=0, padx=5, pady=5, sticky=(N))
    desc2.grid(column=1, row=0, padx=5, pady=5, sticky=(N))

    entry1 = Entry(root, width=20, justify=CENTER, textvariable=env1)
    entry1.grid(column=0, row=1, padx=5, pady=5, sticky=(N))

    entry2 = Entry(root, width=20, justify=CENTER, textvariable=env2)
    entry2.grid(column=1, row=1, padx=5, pady=5, sticky=(N))
    out_display = Label(root, textvariable=out, wraplength=500,
                        justify=CENTER)
    out_display.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky=(N))

    rb = Button(root, text="Calculate", command=_wrap_percentChange)
    rb.grid(row=3, padx=5, pady=5, column=0, sticky=(S))
    cb = Button(root, text="Swap", command=_swap)
    cb.grid(row=3, padx=5, pady=5, column=1, sticky=(S))

    root.bind('<Return>', _wrap_percentChange)
    root.bind('<Escape>', sysexit)

    # Make the window widgets resize automatically
    for x in range(3):
        root.columnconfigure(x, weight=1)
        root.rowconfigure(x, weight=1)
    entry1.focus()
    root.mainloop()
