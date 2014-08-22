# This app is basically a proof of concept of divisibility rules.
# http://en.wikipedia.org/wiki/Divisibility_rule
# All the below functions take integers only!

def isdiv1(n):
    # Any integer is divisible by 1!
    try:
        int(n)
    except:
        return False
    return True
        
def isdiv2(n):
    # If last digit is even, return True
    if list(str(n))[-1] in ['0', '2', '4', '6', '8']:
        return True
    return False

def isdiv3(n):
    # If the sum of the digits is divisible by 3, return True
    if sum(map(int, str(abs(n)))) % 3 == 0:
        return True
    return False

def isdiv4(n):
    # If the last two digits are divisible by 4, return True
    if int(''.join(list(str(n))[-2:])) % 4 == 0:
        return True
    return False

def isdiv5(n):
    # If last digit is 5 or 0, return True
    if list(str(n))[-1] in ['0', '5']:
        return True
    return False
    
def isdiv6(n):
    if isdiv2(n) and isdiv3(n):
        return True
    return False

def isdiv7(n):
    # Subtract 2 times the last digit from the rest. If this is divisble by 7,
    # return True.
    digits = list(str(abs(n)))
    # print digits
    if len(digits) > 1:
        lastdigit = digits[-1]
        rest = ''.join(digits[:-1])
        # print rest, lastdigit, int(rest) - int(lastdigit)*2, (int(rest) - int(lastdigit)*2) % 7
        if (int(rest) - int(lastdigit)*2) % 7 == 0: 
            return True
    elif n == 0 or abs(n) == 7:
        return True
    return False

def isdiv8(n):
    # If the last three digits are divisible by 8, return True
    if int(''.join(list(str(n))[-3:])) % 8 == 0:
        return True
    return False
    
def isdiv9(n):
    # If the sum of the digits is divisible by 9, return True
    if sum(map(int, str(abs(n)))) % 9 == 0:
        return True
    return False
    
def isdiv10(n):
    # If last digit is 0, return True
    if list(str(n))[-1] == '0':
        return True
    return False