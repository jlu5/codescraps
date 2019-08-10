#!/usr/bin/python3
"""
rpsgui.py: graphics.py-based frontend for Rock Paper Scissors.

Copyright (c) 2015-2016, James Lu

License: GPL3+. See LICENSE.GPL3
"""
from rps import *

import os
import graphics

# Sets the directory where images are stored
image_dir = os.path.join(os.getcwd(), 'image_res')

class RPSGUI():
    """
    GUI Rock-Paper-Scissors game using John Zelle's graphics.py and Tkinter.
    """
    def __init__(self):
        # Initialize win, loss, and tie counters.
        self.wins = 0
        self.losses = 0
        self.ties = 0

        # Initialize our window object.
        self.win = graphics.GraphWin('Rock-Paper-Scissors', 600, 500)

        # Maps the RPS item names to their respective images. The values start
        # off as strings representing the filename of each image, but later
        # get replaced by the actual image objects in choose_screen().
        self.images = {'Rock': 'rock.gif', 'Paper': 'loose-leaf-pape-sm.gif',
                       'Scissors': 'nicubunu-Scissors.gif'}

    def is_image(self, point):
        """
        Returns whether the point that was just clicked is part of a drawn image.

        This works by checking whether the point clicked matches a box, formed
        around the anchor (centre) of the image, which has the same height and width
        of the image:

        (x-width/2, y-height/2)                   (x+width/2, y-height/2)
                  *_________________________________________*
                  |                                         |
                  |                                         |
                  |                                         |
                  |                                         |
                  |       image anchor (center) point       |
                  |                 (x, y)                  |
                  |                                         |
                  |                                         |
                  |                                         |
                  |                                         |
                  *_________________________________________*
        (x-width/2, y+height/2)                   (x+width/2, y+height/2)
        """

        # Get the X and Y coordinates of point that was clicked.
        horiz_pos = point.getX()
        vert_pos = point.getY()

        # Check every (item, image) pair we have. For each of them:
        for item, image_obj in self.images.items():

            # 1) Get the center of the image object.
            image_center = image_obj.getAnchor()

            # 2) Get the image dimensions (size of box).
            image_width = image_obj.getWidth()
            image_height = image_obj.getHeight()

            # 3) Check whether the X and Y coordinates of the clicked point
            #    match the box formed. e.g. The horizontal position has to be
            #    between the image anchor minus half the image width, and the
            #    image anchor plus half the image width.
            x_matches = (image_center.getX()-image_width/2) < horiz_pos < \
                        (image_center.getX()+image_width/2)
            y_matches = (image_center.getY()-image_height/2) < vert_pos < \
                        (image_center.getY()+image_height/2)

            if x_matches and y_matches:  # If this matches, return the item name
                return item

    def undraw_all(self):
        """
        Undraws all image and text objects from the previous screen, if they exist.
        """
        try:  # Undraw text from previous screens if present.
            self.text.undraw()
            self.text1.undraw()
            self.text2.undraw()
            self.text3.undraw()
            self.user_img.undraw()
            self.comp_img.undraw()
        except AttributeError:  # Object doesn't exist yet.
            pass

        for image in self.images.values():
            try:  # Try to undraw imaged if they're drawn already.
                image.undraw()
            except AttributeError:  # Object doesn't exist yet.
                pass

    def choose_screen(self):
        """
        Resets the window object given for the rock paper scissors game to the
        "choosing an item" screen.
        """
        # Set the horizontal distance between the images and the window border.
        # This is incremented as each item is drawn. 100 is a decent value for a
        # window size of 600x500.
        width_offset = 100

        self.undraw_all()  # Undraw everything from the previous screen first.

        # Save the description text as an attribute in the window object, so we
        # can access it later.
        self.text = graphics.Text(graphics.Point(300, 120),
                                 "Play Rock-Paper-Scissors against the\n evil "
                                 "machine!\n\nClick on an object below to choose it.")
        # Set the text size to something more readable.
        self.text.setSize(24)
        self.text.draw(self.win)

        self.text1 = graphics.Text(graphics.Point(300, 270),
                    "Times won: %s    Times lost: %s    Times tied: %s"
                    % (self.wins, self.losses, self.ties))
        self.text1.setSize(16)
        self.text1.draw(self.win)

        for item, image in sorted(self.images.items()):
            # Iterate over every image we'll draw
            if type(image) == str:
                # The values of the item name to image ("images") dict defaults
                # to strings with the filename of each picture. Here, they get
                # replaced by the actual image objects.

                # Get the point where we are to draw the image.
                point = graphics.Point(width_offset, 400)

                # Join the image path together.
                image_path = os.path.join(image_dir, image)

                # We need to store these image objects somewhere so it's
                # retrievable, and we can undraw/redraw it later.
                image_obj = self.images[item] = graphics.Image(point, image_path)
            else:
                # Otherwise, because we've already created the image object, we
                # can just draw it again.
                image_obj = self.images[item]

            image_obj.draw(self.win)
            width_offset += 200  # Increase the offset for the next image

        # Now, indefinitely check for whether the point we've clicked is on
        # one of the items. If this matches, return the item name (i.e., what
        # is_image() gives us).
        while True:
            rpsitem = self.is_image(self.win.getMouse())
            if rpsitem:  # is_image() will return the item name if it succeeds
                return rpsitem

    def play(self, user_choice):
        """
        Given the window object for the rock paper scissors game, plays a round
        against the computer with the current item.
        """
        # Turn the user's choice into an RPS Item Object.
        user_object = RPSObject(user_choice)

        # Computer randomly chooses something.
        computer_choice = choose_random()
        computer_object = RPSObject(computer_choice)

        # Initialize the "playing" screen. First, undraw all images and text from
        # the previous screen.
        self.undraw_all()

        text_point = graphics.Point(300, 70)

        # Compare the various RPS item objects to check for wins.
        if user_object == computer_object:  # Tie!
            # Replace the text variable to say this.
            self.text = graphics.Text(text_point, "Tie!")
            self.ties += 1
        elif user_object > computer_object:  # You win! >:(
            self.text = graphics.Text(text_point, "You win!")
            self.wins += 1
        elif user_object < computer_object:  # You lose! >:)
            self.text = graphics.Text(text_point, "You lose!")
            self.losses += 1

        self.text.setSize(32)
        self.text.draw(self.win)

        # Lay out the text portion of the UI by creating the various text
        # labels...
        self.text1 = graphics.Text(graphics.Point(150, 160),
                                   "Computer choice:")
        self.text1.setSize(20)
        self.text1.draw(self.win)

        self.text2 = graphics.Text(graphics.Point(450, 160),
                                   "User choice:")
        self.text2.setSize(20)
        self.text2.draw(self.win)

        self.text3 = graphics.Text(graphics.Point(300, 450),
                                   "Click anywhere to play again.")
        self.text3.setSize(16)
        self.text3.draw(self.win)

        # Now, we need to draw all the pictures representing the user and
        # computers' choices.
        # Create a copy of the existing RPS object images and move them to new
        # coordinates. Unfortunately, graphics.py only seems to support moving
        # things RELATIVE to the image's old coordinates... So we need to
        # subtract the NEW coordinates from the old one to get the images into
        # the positions we want.

        # Get the image representing the computer's choice.
        self.comp_img = self.images[computer_choice].clone()
        comp_img_anchor = self.comp_img.getAnchor()  # Get center of old image

        # Fetch the x and y coordinates of the image
        comp_imgx, comp_imgy = comp_img_anchor.getX(), comp_img_anchor.getY()

        # Move it by the offset needed (new coordinates - old coordinates)
        self.comp_img.move(150-comp_imgx, 300-comp_imgy)

        # Finally, draw the cloned image.
        self.comp_img.draw(self.win)

        # Repeat for the user's choice.
        self.user_img = self.images[user_choice].clone()
        user_img_anchor = self.user_img.getAnchor()
        user_imgx, user_imgy = user_img_anchor.getX(), user_img_anchor.getY()
        self.user_img.move(450-user_imgx, 300-user_imgy)
        self.user_img.draw(self.win)

        # Finally, stay at this screen until the next click.
        self.win.getMouse()

if __name__ == '__main__':  # If we're being ran directly (not imported), play

    # Initialize the game class!
    game = RPSGUI()

    while True:  # Play indefinitely, until window is closed.
        choice = game.choose_screen()  # Get the user choice
        game.play(choice)  # Play it against the computer.