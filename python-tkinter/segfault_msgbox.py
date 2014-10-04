# Rewrite of my earlier segfault_msgbox.vbs in a language that isn't so 
# frustratingly difficult to use ;)
import Tkinter
import tkMessageBox
import random
from _randapp import randapp

Tkinter.Tk().withdraw()

rn = hex(random.randint(1,4294967295))[2:10].zfill(8)
tkMessageBox.showerror(randapp()+" - Application Error",
    "The instruction at 0x%s referenced memory at 0x00000000. The "
    "memory could not be read.\n\nClick on OK to terminate the program" % rn)