import base64
import sys

if len(sys.argv) < 3:
    print("not enough arguments supplied (need 2: inputfile, outputfile)")
    sys.exit(1)

try:
    with open(sys.argv[1], "rb") as image_file:
        image_data = base64.b64encode(image_file.read())
except IOError as e:
    print("Caught IOError: " + str(e))
    sys.exit(1)

try:    
    with open(sys.argv[2], "w") as fout:
        fout.write(image_data)
except Exception as e:
    print("Caught IOError: " + str(e))
    sys.exit(1)