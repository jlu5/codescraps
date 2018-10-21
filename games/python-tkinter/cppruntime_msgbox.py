#!/usr/bin/env python2
import tkinter
import tkinter.messagebox
from _randapp import randapp

tkinter.Tk().withdraw()

tkinter.messagebox.showerror("Microsoft Visual C++ Runtime Library",
    "Runtime Error!\n\nProgram: C:\Windows\System32\%s\n\n\nThis "
    "application has requested the Runtime to terminate it in an "
    "unusual way. \nPlease contact the application's support team for"
    " more information." % randapp())
