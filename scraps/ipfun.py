# Some IP/CIDR calculator thing I'm trying to make. This is probably broken in more places then you can possibly count!

import random
def randip():
    R = []
    for item in range(4):
        R.append(str(random.randint(1, 255)))
    return ".".join(R)
    
def ip2binary(ip):
    L = []
    for bit in ip.split("."):
        L.append((bin(int(bit)).split("b")[1]).zfill(8))
    return L
    
def tobinary(i):
    return bin(i).split("b")[1]
    
def bits2dec(bits):
    L = []
    for bit in bits:
        L.append(int(bit, base=2))
    return L
    # return int(binary, base=2)
    
def splitup(bits):
    L = []
    bits = [str(bit) for bit in bits]
    L.append("".join(bits[0:7]))
    L.append("".join(bits[8:15]))
    L.append("".join(bits[16:23]))
    L.append("".join(bits[24:31]))
    return L
    
# def cidr2ip(cidr):
    # c = cidr.split("/")
    # binaryIP = ip2binary(c[0])
    # subnet = int(c[1])
    # prefix = "".join(binaryIP)[:-(32-subnet)]
    # L = []
    # for i in range(2**(32-subnet)):
        # ip = bits2dec(prefix + tobinary(i).zfill(32-subnet))
        # ip = splitup(ip)
        # L.append(ip)
    # return L
    
for n in range(random.randint(5, 10)):
    IP = randip()
    print "%s / %s / %s / %s " % (IP, "".join(ip2binary(IP)), bits2dec("".join(ip2binary(IP))), len(bits2dec("".join(ip2binary(IP)))))

# cidr = raw_input("CIDR: ")
# cidr = "255.0.0.0/26"
# print(" ".join(cidr2ip(cidr)))
# print "///"
# print cidr2ip(cidr)