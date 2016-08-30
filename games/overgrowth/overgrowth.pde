/*
Overgrowth - a race to the finish! Requires Processing 3.
*/

/* BEGIN GAME CONFIGURATION */
static int tilesize = 40; // Default tile size is 40x40 pixels
static int mapsize = 15; // Default map size is 15x15

// Sets the time in milliseconds the player gets to make it to the finish each round.
static int time_to_finish = 10 * 1000;

// Sets the amount of time added to game time every time the player wins.
static int time_added_each_round = 2 * 1000;

// Set the amount score is incremented on every win.
static int score_increment = 10;

/* Sets the chance of the game picking a random tile to change to grass every time
 * the player reaches the finish (if the game picks a tile that's already grass,
 * nothing happens).
 * 0 is never, 1 is always; 0.6 here would mean 60% of the time.
 */
static double destroy_road_chance = 0.6;

// Sets the various tile colours for road, finish, and grass tiles.
static int road_colour = 0xFF888888;
static int finish_colour = 0xFFFF8800;
static int grass_colour = 0xFF00FF00;

/* END GAME CONFIGURATION */

import java.util.Date;
DrivingGame game;

// Player class (the little blue car)
class Car{
    /* Initialize the car in the middle of the top left tile
     * Graphically, the x and y coordinates are the tile size divided by two,
     * but the actual grid positions (with regards to the world map)
     * would start at (0, 0).
     */
    int xloc = tilesize/2; // x location on actual display
    int yloc = tilesize/2;
    int xgrid = 0;  // x location in grid
    int ygrid = 0;

    void draw() {
        fill(0xFF0088FF); // #0088FF is a light blue colour

        /* From processing docs:
         *
         * ellipseMode(CORNER) interprets the first two parameters of ellipse()
         * as the upper-left corner of the shape, while the third and fourth parameters
         * are its width and height.
         */
        ellipseMode(CENTER);

        // Draw the car as a simple circle that's half the size of each tile.
        ellipse(xloc, yloc, tilesize/2, tilesize/2);
    }

    void move(int x, int y){
        // Increments the position of the car in the given directions

        // Change the graphical position of the car, using the tile size.
        xloc += (x * tilesize);
        yloc += (y * tilesize);

        // Change the grid positions used internally, with regards to the world map.
        xgrid += x;
        ygrid += y;
    }

}


class DrivingGame {
    /* Generates the map and creates the player (car object). The map is simply a
     * two-dimensional array of arrays. Values can be accessed via map[x_coordinate][y_coordinate],
     * and can be any value between 0 and 2 (inclusive).
     */
    int[][] map = makeMap();
    Car car = new Car();

    /* If this time is reached, the player will run out of time and it'll be game over.
     * At the end of each round, some extra time is added to this.
     */
    long finish_time = new Date().getTime() + time_to_finish;

    /* Saves the location of the current finish point (2 length array of x, y coords),
     * along with the previous value it held, before it was turned into the finish point.
     */
    int[] finishpoint = new int[2];
    // This initializes to an invalid value to mean that it hasn't been used by the game yet.
    int finishpoint_lastvalue = -1;

    // Score begins at zero.
    int score = 0;

    // Sets whether we should show all the GAME OVER stuff.
    boolean gameover = false;

    int[][] makeMap() {
        /* Generates a map based on the map size given.
         * Each EVEN row is all road, while each ODD row alternates between road and grass.
         *
         * In other words, the map basically looks like this (where R is road and X is
         * inaccessible grass:
         * R R R R R
         * R X R X R
         * R R R R R
         * R X R X R
         * R R R R R
         *
         * Internally, a grid value of 0 is used for grass, 1 is used for road, and 2 is
         * used for the finish point.
         */

        int[][] map = new int[mapsize][mapsize];
        // Iterate over all rows and columns to generate the map
        for (int row=0; row<mapsize; row++) {
            for (int column=0; column<mapsize; column++) {

                if (row % 2 == 0) {
                    // Even row (divisible by 2) - everything is road
                    map[column][row] = 1;
                } else {
                    /* Odd numbered row. If the column is even,
                     * make the tile grass. Otherwise, make it road.
                     */
                    if (column % 2 == 0) {
                        map[column][row] = 1;
                    } else {
                        map[column][row] = 0;
                    }

                };
            };
        };
        return map;
    };

    void drawMap() {
        /* Draws the map onto the screen. This iterates over all the grid points,
         * row-by-row, using differently coloured tiles to draw each type of point.
         * The xcoord and ycoord variables tell where (on the screen) to draw the
         * tile for the point we're on, and is incremented by the tile size after
         * drawing each point.
         */
        int xcoord = 0, ycoord = 0;
        for (int row=0; row<mapsize; row++) {
            for (int column=0; column<mapsize; column++) {
                if (map[column][row] == 0) { // 0 = grass
                    fill(grass_colour);
                } else if (map[column][row] == 1) { // 1 = road
                    fill(road_colour);
                } else if (map[column][row] == 2) { // 2 = finish
                    fill(finish_colour);
                }
                rect(xcoord, ycoord, tilesize, tilesize);
                xcoord += tilesize;
            };
            // After drawing the end of each row, reset the column count to zero.
            xcoord = 0;

            ycoord += tilesize;
        };
    };

    int[] randomPoint() {
        // Returns a random point on the map.
        int x = int(random(0, mapsize));
        int y = int(random(0, mapsize));
        int[] point = {x, y};
        return point;
    }

    void makeFinishPoint() {
        // Creates a new finish point.

        /* First, set the previous finish point (if it exists) back to the
         * value it had before it was made a finish point (grass or road).
         */
        if (finishpoint_lastvalue != -1) {
            int lastx = finishpoint[0]; // Get the x, y coords of the last
            int lasty = finishpoint[1]; // finish point.
            map[lastx][lasty] = finishpoint_lastvalue;
        }

        /* Now, choose a random point on the map and set that as the finish.
         * Back up the original value as finishpoint_lastvalue, so it is set
         * back to either road or grass on the next call of makeFinishPoint().
         */
        int[] point = randomPoint();
        int x = point[0];
        int y = point[1];

        finishpoint_lastvalue = map[x][y];
        finishpoint[0] = x;
        finishpoint[1] = y;
        map[x][y] = 2;
    }

    void checkFinish() {
        /* Checks whether the player is in a winning position. If true, add to their score
         * and create a new finish point.
         */
        if (car.xgrid == finishpoint[0] && car.ygrid == finishpoint[1]) {
            score += score_increment; // amount to add to score is adjustible (see beginning of file)
            finish_time += time_added_each_round; // ditto with the time to add after reaching each finish
            makeFinishPoint();

            /* After every round, there's a chance that a random road block will be replaced with grass.
             * This means that the path to the finish gets more complex with time, and it's up to players
             * to keep up with the pace!
             */
            int[] rand_point = randomPoint();
            int rand_x = rand_point[0];
            int rand_y = rand_point[1];

            // Only destroy road tiles - if we randomly choose a tile that's already
            if (map[rand_x][rand_y] == 1 && random(0, 1) <= destroy_road_chance) {
                map[rand_x][rand_y] = 0;
            }
        }
    }

    long checkTimer() {
        /* Checks the timers to make sure that the player hasn't lost because they ran out
         * of time, returning the time remaining for them either way.
         */
        long current_time = new Date().getTime();
        long time_remaining = finish_time - current_time;
        println("finish time: " + finish_time + "; current time: " + current_time + "; time remaining: " + time_remaining);

        // Oh no, the player ran out of time!
        if (time_remaining < 0) {
            gameover = true;
        }

        return time_remaining;
    }

}

void settings() {
    // Set up the screen size and window title
    size(800, 600);
}

void setup() {
    // Initialize an instance of our game class.
    game = new DrivingGame();

    frameRate(15);
    frame.setTitle("Overgrowth - a race to the finish!"); // Set window title
    game.makeFinishPoint();
    textAlign(CENTER);
}

void draw() {
    background(250); // Clear game window to prevent duplicate drawings
    int x = game.car.xgrid; // Get the x and y positions of the player (car)
    int y = game.car.ygrid;

    // Move the truck based on the key that has been pressed.
    if (keyPressed) {
        int[][] map = game.map;
        if (!game.gameover) { // Only allow moving if the game hasn't ended already
            try {
                if (keyCode == RIGHT && map[x+1][y] != 0) {
                    game.car.move(1, 0);
                } else if (keyCode == LEFT && map[x-1][y] != 0) {
                    game.car.move(-1, 0);
                } else if (keyCode == UP && map[x][y-1] != 0) {
                    game.car.move(0, -1);
                } else if (keyCode == DOWN && map[x][y+1] != 0) {
                    game.car.move(0, 1);
                } else if (key == ' ') {
                    /* Press space to generate a new finish point, if the
                     * player encouters an unreachable finish point surrounded
                     * by walls.
                     */
                    game.makeFinishPoint();
                }
            } catch (IndexOutOfBoundsException e) {
                // If we hit the edge of the map, just return.
            }
        } else if (key == ' ') {
            setup();
            return;
        }
        println("Drew car at " + x + ", " + y + " at (" + game.car.xloc + ", " + game.car.yloc + ")");
        println("Finish point is " + game.finishpoint[0] + ", " + game.finishpoint[1]);
    }

    // Check if the player has reached the finish. If so, create a new one.
    game.checkFinish();

    // Draw the map and the player on screen.
    game.drawMap();
    game.car.draw();

    // Write all the text for the rest of the GUI.
    fill(10);
    textSize(32);

    text("Score", 700, 75);
    text(game.score, 700, 125);

    if (game.gameover) {
        text("GAME OVER", 700, 210);
        // Here, text is manually broken so it fits properly in the window sidebar.
        text("Press space\nto restart.", 700, 310);
    } else {
        text("Time\nremaining: ", 700, 210);
        long time_remaining = game.checkTimer();

        /* Display the time remaining in seconds: time_remaining gives milliseconds
         * by default.
         */
        long seconds_remaining = round(time_remaining/1000);
        text(seconds_remaining + " seconds", 700, 310);
    }

    textSize(18);
    text("Use arrow keys to\nmove. Press space to\ncreate a new finish\npoint if you're stuck\nin an impossible\nposition.", 700, 400);

}