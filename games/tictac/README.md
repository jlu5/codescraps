A command line Tic-Tac-Toe / Gomoku game with adjustable board size.

To start, run `python ttt.py` or `run.bat` (for Windows users with Python in the PATH).
Various options can be set via command-line arguments, such as board height + width, amount of markers needed by a player in a row to win, etc. Help is given by running `ttt.py` or `run.bat` with the `--help` or `-h` arguments.

Since the sides of the Tic-Tac-Toe board are adjustable, there are numerous possible board setups! Some interesting combinations include 5x5x4 (5 by 5 board where you need 4-in-a-row to win), or a Gomoku-style 15x15x5.

Custom player names, along with more than 2 players, can be defined via the `--players` or `-p` options. For example, `ttt.py --players Joe Alex Sam` adds players named "Joe", "Alex", and "Sam" to the game. Player names can be anything; they are not limited to X's and O's!

The order in which players move can be shuffled using the `--shuffle` or `-s` options (this is not done by default).

```
usage: ttt.py [-h] [--no-color] [--players [PLAYERS [PLAYERS ...]]]
              [--shuffle]
              [width] [height] [items]

Command line Tic-Tac-Toe game with adjustable sides.

positional arguments:
  width                 sets game board width
  height                sets game board height
  items                 sets amount of places in a row needed to win a game

optional arguments:
  -h, --help            show this help message and exit
  --no-color, -nc       disables grid colouring in the game
  --players [PLAYERS [PLAYERS ...]], -p [PLAYERS [PLAYERS ...]]
                        selects player names (2 or more)
  --shuffle, -s         defines whether the players should be shuffled
```