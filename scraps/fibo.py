def fib(n): # write Fibonacci series up to n
    a, b = 0, 1
    while b < n:
        print b,
        a, b = b, a+b

def fib2(n): # return Fibonacci series up to n
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result

if __name__ == "__main__": # If not an import
    import sys
    try:
        s = sys.argv[1]
    except IndexError: # If no argument:
        s = raw_input("Type a number to return a"
            " Fibonacci series up to: ")
    try: 
        fib(int(s))
    except ValueError:
        print 'That\'s not a valid number!'
