#!/usr/bin/env python3
# Rewrite of my earlier segfault_msgbox.vbs in a language that isn't so
# frustratingly difficult to use ;)
import tkinter
import tkinter.messagebox
import random
from _randapp import randapp

tkinter.Tk().withdraw()

rn = hex(random.randint(1,4294967295))[2:10].zfill(8)
tkinter.messagebox.showerror(randapp()+" - Application Error",
    "The instruction at 0x%s referenced memory at 0x00000000. The "
    "memory could not be read.\n\nClick on OK to terminate the program" % rn)
