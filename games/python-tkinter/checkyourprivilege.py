#!/usr/bin/env python3
"""
Python + Tkinter app for checking your privilege.
"""

import random
from tkinter import *
from tkinter.ttk import *
import time

privileges = ("Extremely oppressed", "Severely oppressed", "Very oppressed",
              "Oppressed", "Spoiled", "Very spoiled", "Severely spoiled",
              "Extremely Spoiled")

class CheckYourPrivilege():
    """
    Creates an instance of the privilege checker.
    """
    def __init__(self):
        self.root = Tk()
        self.root.title("Privilege Checker")
        self.root.geometry('600x400')  # Set default window size.
        self.root.minsize(300, 200)  # Set MINIMUM window size.

        # Stores the last generated "privilege" as a string.
        self.privilege = StringVar()

        # Surround all the elements with a frame for padding purposes
        self.frame = Frame(height=5)
        self.frame.pack(fill=BOTH, padx=20, pady=45, expand=1)

        # Button to "Check My Privilege"
        self.button = Button(self.frame, text="Check My Privilege",
                             command=self.update_privilege)
        self.button.pack(fill=BOTH, expand=1, padx=10, pady=10)

        # Label to display the output
        self.privilege_display = Label(self.frame, text="", anchor=CENTER,
                                       textvariable=self.privilege,
                                       font=("Helvetica", 16))
        self.privilege_display.pack(fill=BOTH, expand=1, padx=10, pady=10)

        mainloop()

    def update_privilege(self):
        """
        Updates the privilege text field.
        """
        priv = random.choice(privileges)
        time.sleep(0.005)  # Make button spamming APPEAR less laggy

        # Set the storage field to what we randomly chose; the label will
        # update automatically!
        self.privilege.set(priv)

if __name__ == "__main__":
    cyp = CheckYourPrivilege()
