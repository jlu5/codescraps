from math import factorial
try: print factorial(int(float((raw_input("Type integer to get factorial of: ")))))
except ValueError: print("THAT'S NOT A POSITIVE INTEGER YOU FOOL!")
raw_input()
