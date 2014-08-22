from math import pi

def cylinder(r, h):
    V = 1.0*pi*(r**2)*h
    return V
    
def cone(r, h):
    V = (1.0*pi*(r**2)*h)/3
    return V
    
def sphere(r, h):
    V = (1.0*4*pi*(r**3))/3
    return V
    
if __name__ == "__main__":
   while True:
       s = raw_input("Shape?: ")
       r = float(raw_input("radius: "))
       h = float(raw_input("height: "))
       if s == "0":
           print "Volume of cylinder: %s" % cylinder(r, h)
       if s == "1":
           print "Volume of cone: %s" % cone(r, h)
       if s == "2":
           print "Volume of sphere: %s" % sphere(r, h)