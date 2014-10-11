#!/usr/bin/env python2

target = "/usr/share/mate-background-properties/"

import glob
import os.path
import sys

for item in glob.glob("/usr/share/gnome-background-properties/*"):
	tf = target+os.path.basename(item)
	if not os.path.isfile(tf):
		print "{} does not exist in {}, symlinking...".format(item,target)
		os.symlink(item, target+"desymlink00-"+os.path.basename(item))
