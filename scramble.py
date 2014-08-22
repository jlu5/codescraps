from random import shuffle

def scramble(word):
    word = list(word)
    shuffle(word)
    return ''.join(word)
    
if __name__ == "__main__":
    s = raw_input("Enter string to scramble: ")
    print scramble(s)
    raw_input()