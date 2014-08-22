import random
# Responses taken from http://en.wikipedia.org/wiki/Magic_8_ball#Possible_answers
responses = ['It is certain.', 'It is decidedly so.', 'Without a doubt.',
    'Yes definitely.', 'You may rely on it', 'As I see it, yes.',
    'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
    'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
    'Cannot predict now.', 'Concentrate and ask again.',
    'Don\'t count on it.', 'My reply is no.', 'My sources say no.',
    'Outlook not so good.', 'Very doubtful.']

def eightball(question=''):
    """Ask the Magic 8-ball a question!"""
    return random.choice(responses)
    
if __name__ == "__main__": # If not an import:
    import sys
    if len(sys.argv) <=1: # This is just to add a touch of realism
        raw_input("Think of a question, and let the magic 8-ball find the answer:\n\n")
    print random.choice(responses) # The Magic of randomness!
