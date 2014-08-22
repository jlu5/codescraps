import random

t, n = 0, random.randint(1, 1000)
print("Let's play HiLo!")

while True:
    try:
        try:
            g = int(raw_input("Pick a number between 1 and 1000: "))
        except ValueError:
            print("That's not even a number!\n")
            continue
        if g > n:
            print "Lower!"
            t = t + 1
        elif g < n:
            print "Higher!"
            t = t + 1
        else:
            if t == 1:
                print('What... It took just 1 try for you to get {}...'.format(n))
            print('You win! The correct number was {} and it took you {} tries to'
                 ' find it!'.format(n, t))
            break
    except KeyboardInterrupt:
        print('\nExiting...')
        break