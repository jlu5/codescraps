from PIL import Image
import sys
try:
    from os import startfile
except ImportError:
    from subprocess import call
    
    def startfile(filename):
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        call([opener, filename])

if sys.version_info[0] >= 3:
    raw_input = input

color = raw_input("Pick a color to output an image: ")
im = Image.new("RGB", (256, 256), color)
im.save("imgm.png")
startfile("imgm.png")
