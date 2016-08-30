"""
morecircles.py: Draws concentric circles, but only when asked to.

License: GPL3+. See LICENSE.GPL3
"""

import graphics
import random
import time

def circles(width=360, height=360):
    """Creates a window drawing concentric circles."""
    win = graphics.GraphWin('Concentric circles', width, height)

    shapes = []

    # Create a circle in the windows' center
    text = graphics.Text(graphics.Point(width/2, height/2), 'Click somewhere to draw!')
    text.draw(win)
    while True:  # Run the drawing loop forever

        point = win.getMouse()
        text.undraw()

        # Sleep between runs for extra effect
        time.sleep(random.uniform(0.05, 0.10))

        while shapes:
            # Undraw all existing shapes before drawing the new ones.

            # list.pop() removes and returns the first item from the shapes
            # list, which in this case is the graphics.Circle object, that we
            # can undraw.
            shapes.pop().undraw()

        # Draw between 50-135 circles (randomly chosen)
        for circle in range(5, random.randint(50, 135)):
            # Each circle (I call it "ball" here) is created with a center
            # point of where the user clicks, and a randomly chosen radius.

            ball = graphics.Circle(point, circle)
            ball.draw(win)

            # Randomly choose colour (for effect) out of:
            ball.setOutline(random.choice([
                '#AAA', '#111', '#888', '#333', '#CCC', # Various shades of grey,
                '#11CCEE', '#1144BB', # Shades of blue
                '#5511CC', # Purple,
                '#EEFF11', # Lime green,
                '#AA1111', # and dark red.
            ]))

            # Add the shape to the "shapes" list, so we can remove it in the
            # next run.
            shapes.append(ball)

if __name__ == '__main__':
    # If the program was started in the command line, run the circles
    # generation.
    circles()