#!/usr/bin/env python3

from tkinter import *
from tkinter.ttk import *
from sys import exit as sysexit

import hexip
import unhexip

if __name__ == "__main__":
    root = Tk()
    root.title("Hex / Unhex IP")

    out, ip = [StringVar() for _ in range(2)]

    def _pack(obj, **kwargs):
        obj.pack(padx=5, pady=5, expand=True, **kwargs)

    def _wrap(func):
        value = ip.get()
        if value:
            try:
                out.set(func(value))
            except ValueError as e:
                out.set("ValueError: %s" % e)
        else:
            out.set("No IP / hex string input!")

    def _wrap_hexip(*args):
        _wrap(hexip.hexip)

    def _wrap_unhexip(*args):
        _wrap(unhexip.unhexip)

    frame = Frame(root)
    #frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
    _pack(frame, fill=BOTH)

    # Buttons
    unhex_btn = Button(root, text="Unhex", command=_wrap_unhexip)
    _pack(unhex_btn, side=RIGHT)
    hex_btn = Button(root, text="Hex", command=_wrap_hexip)
    _pack(hex_btn, side=RIGHT)

    # Entry field
    ip_entry = Entry(frame, justify=CENTER, textvariable=ip)
    _pack(ip_entry, fill=BOTH)

    # Output display
    out_display = Entry(frame, textvariable=out, width=50, justify=CENTER, state="readonly")
    _pack(out_display, fill=BOTH)

    root.bind('<Escape>', sysexit)

    ip_entry.focus()
    root.mainloop()
