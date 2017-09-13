#!/usr/bin/python3
"""
rps.py: Classes for Rock Paper Scissors.

Copyright (c) 2015-2016, James Lu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import print_function
import random
import functools

choices = ['Rock', 'Paper', 'Scissors']

def choose_random():
    """
    Chooses a random RPS item for the computer to play.
    """
    return random.choice(choices)

def play_cli():
    """
    Interactively plays RPS against the computer.
    """
    # Randomly choose something for the computer to throw.
    computer_choice = choose_random()

    # This maps responses to the actual item name.
    user_choices = {'s': 'Scissors', 'r': 'Rock', 'p': 'Paper'}

    while True:  # Check for valid responses in a loop.
        try:
			# .lower() takes the string and returns it in lowercase.
            user_choice = input('What would you like to throw? '
			                    '(s=Scissors, r=Rock, p=Paper) ').lower()

            # Choose the appropriate one from the user input.
            user_choice = user_choices[user_choice]
            break
        except KeyError:
            print("I'm not quite sure what that is, try again.")
        print()  # Extra newline for prettier output.

    # Create RPSObject (below) instances for both the computer and the user's
    # choices. These objects allow us to compare choices easily.
    computer_rps = RPSObject(computer_choice)
    user_rps = RPSObject(user_choice)

    print()
    print("You throw %s." % user_choice)
    print("Computer chose %s." % computer_choice)
    print()

    # Compare the various RPS objects.
    if user_rps > computer_rps:  # Your choice was greater than the computer's
        print("%s beats %s, you win!" % (user_choice, computer_choice))
        return True
    elif user_rps == computer_rps:  # Computer chose the same thing as you
        print("Tie, try again.")
    else:  # You lose :(
        print("%s beats %s, you lose!" % (computer_choice, user_choice))

# This lovely wrapper in Python 2.7 and 3.2+ fills in all the various
# comparison operators given only two (in this case, __gt__ and __eq__).
@functools.total_ordering
class RPSObject():
    """
    Class implementing a rock, paper, scissors choice. This can be used to
    compare with other objects of the same type, using the Python comparison
    operators (>, <, ==, etc.).
    """
    def __init__(self, obj):
        self.choices = choices

        # This stores the type of object we are (rock, paper, or scissors).
        self.obj = obj

        # The list.index function returns where we are within the choices list.
        self.index = self.choices.index(obj)

    def __gt__(self, other):
        """
        Returns whether this RPSObject instance wins against the opponent's
        choice given. This overloads the ">" comparison operator.
        """
        # This evaluates to True if either the index (place in the "choices"
        # list) of our object subtracted by the index of the opponent's object
        # equals 1, or our object is the first object (index 0) and the
        # opponent's is the last (index 2).
        #  e.g. The index of Paper (1) - the index of Rock (0) = 1;
        #       thus paper beats rock and this returns True.
        if self.index - other.index == 1:
            return True
        elif self.index == 0 and other.index == len(choices)-1:
            return True
        return False

    def __eq__(self, other):
        """
        Returns whether the two given RPSObject instances represent the same
        thing. This overloads the "==" comparison operator.
        """
        return self.obj == other.obj  # Simply match the object name

if __name__ == '__main__':
    # If started directly from command line, play the game.
    print("Play rock paper scissors against the evil machine!")
    print()

    times_won = 0
    times_played = 0

    while True:  # Play indefinitely until program is exited.
        if play_cli():  # This returns True if the player won
            # Increment the times won and the total times played.
            times_won += 1
        times_played += 1

        print("You've won %s time(s) out of %s." % (times_won, times_played))
        print()