import random
# Honestly I have to say I've done this with pretty much every language I've
# experimented with, with varying degrees of success.
# Responses taken from http://en.wikipedia.org/wiki/Magic_8_ball#Possible_answers
responses = ['It is certain.', 'It is decidedly so.', 'Without a doubt.',
    'Yes definitely.', 'You may rely on it', 'As I see it, yes.',
    'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
    'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
    'Cannot predict now.', 'Concentrate and ask again.',
    'Don\'t count on it.', 'My reply is no.', 'My sources say no.',
    'Outlook not so good.', 'Very doubtful.']
    
raw_input("Think of a question, and let the magic 8-ball find the answer.\n")
print ''
print random.choice(responses) # The Magic of randomness!
print ''
raw_input("Press Enter to continue")