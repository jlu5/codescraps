#!/usr/bin/env python3
import sys
from random import choice

class TicTacToe:
    def __init__(self):
        self.grid = dict(enumerate(range(1, 10), start=1))
        if sys.version_info[0] < 3:
            input = raw_input
        # All possible win combinations (horizontal, vertical, diagonal)
        self.combinations = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8),
                             (3, 6, 9), (3, 5, 7), (1, 5, 9)]
        self.players = ('x', 'o')

    def start(self, term=True):
        # Start the game at a random player!
        if term:
            self.play(choice(self.players))
        else:
            # The GUI App or whatever will wrap around this and
            # call playGUI() manually.
            pass

    def _checkWin(self):
        # Check each possible winning combination
        for c in self.combinations:
            for player in self.players:
                if self.grid[c[0]] == self.grid[c[1]] == self.grid[c[2]] == player:
                    print('%s wins!' % player)
                    return 1
        # Check if every grid is used by a player value; if so, it's a tie!
        for c in self.grid.values():
            if c not in self.players:
                break
        else:
            print("It's a tie!")
            return 2

    def showgrid(self):
        print('+---+---+---+')
        print('| %s | %s | %s |' % (self.grid[1], self.grid[2], self.grid[3]))
        print('+---+---+---+')
        print('| %s | %s | %s |' % (self.grid[4], self.grid[5], self.grid[6]))
        print('+---+---+---+')
        print('| %s | %s | %s |' % (self.grid[7], self.grid[8], self.grid[9]))
        print('+---+---+---+')

    def playGUI(self, player, inp):
        if inp not in self.grid.keys():
            raise KeyError("Invalid grid space (must be 1-9).")
        elif self.grid[inp] in self.players:
            raise ValueError("This space is already taken!")
        else:
            self.grid[inp] = player
        if not self._checkWin():
            if player == 'x':
                self.play('o')
            else:
                self.play('x')

    def play(self, player):
        self.showgrid()
        print("\nYou are: %s" % player)
        inp = ''
        while True:
            try:
                inp = int(input("Pick a number on the grid to place your mark: "))
            except (ValueError, IndexError):
                pass
            except KeyboardInterrupt:
                print("\nExiting on Ctrl-C...")
                sys.exit(1)
            print()
            if inp not in self.grid.keys():
                print("Invalid grid space (must be 1-9).")
            elif self.grid[inp] in self.players:
                print("This space is already taken!")
            else:
                self.grid[inp] = player
                break
        if not self._checkWin():
            if player == 'x':
                self.play('o')
            else:
                self.play('x')
        else:
            self.showgrid()

if __name__ == '__main__':
    print("Welcome to Tic-Tac-Toe!")
    game = TicTacToe()
    game.start()