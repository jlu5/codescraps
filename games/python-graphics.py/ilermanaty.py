# ilermanaty.py - draws "ilermanaty" windows inspired by the Illuminati meme.

import graphics
import random

def _get_text():
    """Returns a randomly selected text to go with the drawing."""
    return random.choice(['FEAR ME', 'ilermanaty op', "we're watching u", "look at the eye", "not your average triangle", "muahaha", 'we know everything!',"Bill Ciper was here"])

def ilermanaty():
    """Creates a window with the beautiful "ilermanaty" drawing."""
    win = graphics.GraphWin('ilermanaty', 300, 300)
    
    # Draw a triangle
    triangle = graphics.Polygon([graphics.Point(x, y) for x, y in ((150, 30), (40, 230), (260, 230))])
    triangle.setOutline('DarkSeaGreen')
    
    
    # Draw an oval
    eye = graphics.Oval(graphics.Point(80, 130), graphics.Point(220, 210))
    eye.setFill('DarkSeaGreen')
    
    eyeball = graphics.Circle(eye.getCenter(), 24)
    eyeball.setFill('Black')
    
    text = graphics.Text(graphics.Point(150, 270), _get_text())
    text.setSize(14)
    
    triangle.draw(win)
    eye.draw(win)
    eyeball.draw(win)
    text.draw(win)
    return win

if __name__ == '__main__':
    # Spawn a few for added effect
    for x in range(random.randint(3, 10)):
        win = ilermanaty()
    else:
        win.getMouse()
    