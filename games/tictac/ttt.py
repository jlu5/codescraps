#!/usr/bin/env python
"""
ttt.py: Command line Tic-Tac-Toe / Gomoku with arbitrary board size.
"""

# Use the new-style print() function for forwards compatibility with Python 3.x
from __future__ import print_function
import itertools
from sys import version_info
import random

if version_info[0] >= 3:
    raw_input = input
    xrange = range

from grid import *

class TicTacToe():
    """Tic-Tac-Toe game class."""
    def __init__(self, width=3, height=3, items=3, players=['X', 'O'],
                 use_color=True, shuffle=False):
        # For each game instance, set the width, height, and amount of places
        # a player needs in a row to win.
        assert items <= height and items <= width, ("Amount of places in a "
            "row needed to win must be less or equal to game width and "
            "height.")
        assert items > 2, ("Amount of places in a row needed to win must be "
            "greater than 2.")
        assert width <= 20 and height <= 20, "Game width and height must be <= 20."
        assert len(players) >= 2, "Must have at least 2 players."
        assert all(players), "Player names cannot be empty!"

        self.width = width
        self.height = height
        self.items = items

        # Initialize an instance of the Grid class.
        self.grid = Grid(width, height, use_color=use_color)

        # Shuffle the players before assigning, if requested.
        if shuffle:
            random.shuffle(players)

        self.players = players
        # This creates an iterator that cycles through the players infinitely:
        # X, O, X, O, X, O, X ...
        self.player_cycle = itertools.cycle(self.players)

    def _w(self, x, y):
        """Returns the coordinates west of the point (x, y) given."""
        return (x-1, y)

    def _n(self, x, y):
        """Returns the coordinates north of the point (x, y) given."""
        return (x, y-1)

    def _s(self, x, y):
        """Returns the coordinates south of the point (x, y) given."""
        return (x, y+1)

    def _e(self, x, y):
        """Returns the coordinates east of the point (x, y) given."""
        return (x+1, y)

    def _nw(self, x, y):
        """Returns the coordinates northwest of the point (x, y) given."""
        return (x-1, y-1)

    def _ne(self, x, y):
        """Returns the coordinates northeast of the point (x, y) given."""
        return (x+1, y-1)

    def _sw(self, x, y):
        """Returns the coordinates southwest of the point (x, y) given."""
        return (x-1, y+1)

    def _se(self, x, y):
        """Returns the coordinates southeast of the point (x, y) given."""
        return (x+1, y+1)

    def check_win(self, player):
        """
        Checks whether the given player has won the game with the current
        settings.
        """
        # To check for whether the player has won, see if the N squares away
        # from any position (in any direction) are all filled by the player in
        # question.
        # N is the amount of squares in a row a player must fill in order to
        # win. And since we're using a square board, the possible directions
        # to check are: north, west, south, east, northwest, northeast,
        # southwest, and southeast.
        for position in itertools.product(range(self.width), range(self.height)):
            for direction in ('n', 'w', 's', 'e', 'nw', 'ne', 'sw', 'se'):
                x, y = position
                # Make a list of all points looked at while checking in this
                # direction. This includes the current one to start.

                data = self.grid.get(x, y)
                if not data:  # If the point is empty, skip it
                    continue

                points = [data]
                # Recursively check these squares until we check the amount
                # of squares that the player needs to win.
                for item in xrange(self.items):
                    # Find the appropriate helper functions to get the
                    # coordinates for this direction (_w/_s/_e/etc. functions
                    # above).
                    func = getattr(self, '_%s' % direction)
                    # Replace the x and y coordinates and repeat until we check
                    # enough squares that the player needs to win.
                    x, y = func(x, y)
                    try:
                        # Add the new coordinates to the list of points
                        # checked.
                        data = self.grid.get(x, y)
                        points.append(data)
                    except IndexError:
                        # We overflowed (i.e. hit the side of the board)
                        # while going in a direction, stop.
                        break
                    else:
                        if points == [player]*self.items:
                            # If the player is winning, the end list of points
                            # we checked should be equal to a list of the
                            # player name repeated the amount of items they
                            # need to win (self.items).
                            return True
        else:
            pass
        return False

    def place(self, player, point):
        """
        Places the player at the grid point given, if it is not already
        taken.
        """
        x, y = self.grid.get_coordinates(point)
        self.grid.set(x, y, player)

    def play(self):
        """Main loop to start interactive command line gameplay."""
        # Iterate over the players indefinitely
        for player in self.player_cycle:
            # Show the grid before every move
            self.grid.show()
            # All items are taken and nobody won!
            if all(self.grid.all_items()):
                return None
            print("%s's turn!" % player)
            # Basic error checking: loop infinitely for input until we get a
            # valid value so random text here won't crash our program.
            while True:
                point = raw_input("Enter a place to put your %s marker: " %
                                  player)
                try:
                    point = int(point)
                    self.place(player, point)
                except GridItemFilledError:
                    # Grid item already filled
                    print("That point is already taken!")
                    continue
                except ValueError:
                    # Invalid input (not a number)
                    continue
                except IndexError:
                    # Bad grid point given (i.e. negative or not on the grid)
                    print('Bad point given.')
                    continue
                else:
                    # If everything works, set the last point we placed and
                    # break the loop.
                    break
            if self.check_win(player):
                # Does the player win? If so, return their name and break.
                game.grid.show()
                return player

if __name__ == '__main__': # Program ran from command line
    # argparse is great for parsing command line options!
    # This app can be run with arguments like "ttt.py 5 3" for a 5x5 game
    # where 3 in a row is needed to win.
    import argparse

    # Help is given via "ttt.py --help" or "ttt.py -h".
    parser = argparse.ArgumentParser(description='Command line Tic-Tac-Toe '
                                     'game with adjustable sides.')
    parser.add_argument('width', type=int, nargs='?', default=3,
                        help='sets game board width')
    parser.add_argument('height', type=int, nargs='?', default=3,
                        help='sets game board height')
    parser.add_argument('items', type=int, nargs='?', default=3,
                        help='sets amount of places in a row needed to win a '
                        'game')
    parser.add_argument('--no-color', '-nc', action='store_false',
                        help='disables grid colouring in the game')
    parser.add_argument('--players', '-p', nargs='*', default=['X', 'O'],
                        help='selects player names (2 or more)')
    parser.add_argument('--shuffle', '-s', action='store_true',
                        help='defines whether the players should be shuffled')
    args = parser.parse_args()

    intro_text = 'Tic-Tac-Toe! Place your marker on the grid by typing in the corresponding number.'
    if colorama:  # Colouring is available
        intro_text = colorama.Fore.WHITE + intro_text
    print(intro_text)

    # Initialize a game instance using the options given above
    game = TicTacToe(height=args.height, width=args.width, items=args.items,
                     use_color=args.no_color, players=args.players,
                     shuffle=args.shuffle)
    result = game.play()
    if result is None:
        print("It's a tie!")
    else:
        print("Player %s wins!" % result)