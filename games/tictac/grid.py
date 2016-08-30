"""Grid system using nested lists."""

from __future__ import print_function
import string
import itertools
import re
import sys
from random import shuffle

'''
# This program uses colorama, licensed under the MIT license, for terminal
# colouring. A fallback copy of it is included in the colorama-x.y.z,
# but a globally installed instance will override it. If this is not desired,
# remove the next 2 lines and the colorama folder.
import glob
sys.path += glob.glob('colorama*')
'''

if sys.version_info[0] >= 3:
    raw_input = input
    xrange = range

try:
    import colorama
except ImportError:
    print("Warning: Missing colorama module - colour support will be disabled.")

    colorama = None
    # Colouring not available; make a dummy colourize function that just
    # returns what it's given.
    colourize = lambda text: text
else:
    # Initialize colorama
    colorama.init()

    _available_colors = [colorama.Fore.RED, colorama.Fore.GREEN,
                         colorama.Fore.YELLOW, colorama.Fore.MAGENTA,
                         colorama.Fore.CYAN, colorama.Fore.WHITE]
    # Shuffle the colours every time to give them more variety
    shuffle(_available_colors)
    def colourize(text):
        """Returns a coloured version of the given text based on a hash of its
        characters' sum."""
        charsum = sum(ord(str(char)) for char in text)
        colorcode = _available_colors[charsum % len(_available_colors)]
        return "%s%s%s%s" % (colorama.Style.BRIGHT, colorcode, text, colorama.Style.RESET_ALL)


class GridItemFilledError(ValueError):
    # Raised when a grid point we requested is already filled.
    pass

class Grid():
    """Grid system using nested lists."""
    def __init__(self, width=3, height=3, use_color=True):
        """
        Initialize the grid: a list of lists. The first (big) list is equal
        to the amount of columns in the game. It includes a series of
        sublists, each representing a row in the grid. Each item in the
        sublist represents a space on the grid.

        A 3 by 3 grid would look like, internally:
           [['', '', ''], ['', '', ''], ['', '', '']]
        In this implementation, the origin point (0, 0) is the top left. The
        coordinates for a 3 by 3 grid would thus be the following.
           [[(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)]]

        We need to use list comprehensions instead of simply multiplying a list by
        the width/height, so that each grid point has a distinct reference.
        Otherwise, setting one point in the grid will cause other ones to be
        changed too.
        """
        self.grid = [['' for _ in xrange(width)] for _ in xrange(height)]
        self.width = width
        self.height = height

        self.use_color = use_color

        # Store the length of the largest item that's ever been added to the
        # grid, so that grid cells are formatted with the right widths.
        # 3 is a good default since it gives the grid ample space to start,
        # but it will grow if bigger strings are stored.
        self.largestlength = 3

    def get(self, x, y, allowOverflow=False):
        """Returns the contents of the grid item at (x, y)."""
        if (not allowOverflow) and (x < 0 or y < 0):
            raise IndexError("Grid coordinate is negative.")
        return self.grid[y][x]

    def set(self, x, y, object, allowOverflow=False, allowOverwrite=False):
        """Sets the contents of the grid item at (x, y)."""
        if (not allowOverflow) and (x < 0 or y < 0):
            raise IndexError("Grid coordinate is negative.")
        if (not allowOverwrite) and self.grid[y][x]:
            raise GridItemFilledError("Coordinates requested have already been filled.")

        objectlength = len(object)
        # If the length of the object is greater than the largest length we've
        # seen so far, update the length. This is used for grid formatting
        # purposes, so that each cell has the right width.
        if objectlength > self.largestlength:
            self.largestlength = objectlength
        self.grid[y][x] = object

    def show(self):
        """
        Prints the current grid to screen.

        For unused squares, show the number of the coordinate instead.
        This way, a blank 3 by 3 grid gets shown as:
        |---|---|---|
        | 1 | 2 | 3 |
        |---|---|---|
        | 4 | 5 | 6 |
        |---|---|---|
        | 7 | 8 | 9 |
        |---|---|---|, instead of each item being empty.
        """
        # Print the top bar with the right cell width:
        #    |---|---|---|
        print('|%s' % ('-' * self.largestlength) * self.width + '|')
        # To get the numbers of each grid point, first enumerate every rows'
        # data with their position in the grid:
        #    [(0, <contents of row 1>), (1, <contents of row 2>), (2, <contents of row 3), ...]
        for rowpos, row in enumerate(self.grid, 0):
            # In the same way, enumerate the column index and the data of each
            # grid point in the row:
            #    [(0, <contents of point (0, 0)>),
            #     (1, <contents of point (1, 0)>),
            #     (2, <contents of point (2, 0)>), ...]
            for colpos, char in enumerate(row, 1):
                print('|', end='')
                place = str(rowpos * self.width + colpos)

                # Note:
                # This can be uncommented so that the grid defaults to showing
                # the internal grid position, instead of the numeric position.
                #place = "(%s, %s)" % (colpos-1, rowpos)

                # Make each grid item N characters long, centring it and padding it with spaces.
                # N is always the LARGEST object length we've seen so far, so that the cell
                # has the right width.
                output = char or place
                output = output.center(self.largestlength, ' ')

                if colorama and self.use_color and char:
                    # If colouring is enabled and available, *replace* the
                    # object string with a coloured version. This has to be
                    # done after the padding step, so that the ANSI codes used
                    # for colouring don't mess up the spacing - these codes
                    # take up space in the string too, which will cause to
                    # little whitespace to be added and strange, misaligned
                    # tables to appear.
                    output = output.replace(char, colourize(char), 1)

                print(output, end='')
            print('|')
            print('|%s' % ('-' * self.largestlength) * self.width + '|')
            # Print the dividing bar with the right cell width between every row:
            #    |---|---|---|

    def __iter__(self):
        # This overrides list(Grid()), so that it returns meaningful results instead of an error.
        for item in self.grid:
            yield item

    def __repr__(self):
        # This overrides str(Grid()), so that it gives meaningful results instead of something like <Grid instance at 0x12345678>
        return repr(self.grid)

    def all_items(self):
        """Returns all the items in the grid, reduced into one list."""
        return list(itertools.chain.from_iterable(self.grid))

    def get_coordinates(self, point):
        """Returns the coordinate pair for the grid point (number on grid) given."""
        # Since our grid numbering starts at one, subtract one from the requested point.
        point -= 1
        # Some math magic here: since the grid points flow from left to right and then up to down,
        # The x value is equal to the remainder of the requested point divided by the width, and
        # the y value simply the point divided by width, truncated.
        # In short, this is the divmod() of point and the width, reversed.
        return divmod(point, self.width)[::-1]