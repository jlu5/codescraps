/*
Niceviz! - An audio visualization demo with Processing 3 + Minim.
*/

import ddf.minim.*;
import java.util.*;
import java.io.FileNotFoundException;

//// BEGIN CONFIGURATION

// Determines the amount of lyric lines to show at one time.
int lines_to_show = 3;

public String song_file = "demo.mp3";
public String lyrics_file = "demo.lrc";

//// END CONFIGURATION

// Initialize variables
Minim minim;
AudioPlayer player;
float level;
int[][] color_scheme;
String text;
boolean show_text = true;

ArrayList<LyricPair> lyrics = new ArrayList<LyricPair>();
ArrayList<String> shown_lines = new ArrayList<String>(); // Stores the currently shown lines
int current_position = 0; // Stores the current position in the lyrics list
Integer next_position;
LyricPair lyric_pair;
boolean reached_end = false;
float[] choose_file_coords;
String raw_lines[];

/* Implement a sortable class for lyrics lines: each one stores the time it should
 * be displayed and the corresponding text.
 */
class LyricPair implements Comparable<LyricPair> {

    String text;
    Integer time;

    LyricPair(Integer time_, String text_) {
        // Use this to initialize the time and text variables
        time = time_;
        text = text_;
    }

    int compareTo(LyricPair other) {
        // When comparing, just look at which LyricPair instance has
        // a larger time.
        return this.time.compareTo(other.time);
    }
}

void loadLyrics(String lyrics_file) {

    // First, clear the old lyrics text before adding any more.
    lyrics.clear();
    shown_lines.clear();
    current_position = 0;

    // Load the lines of the lyrics file using the Processing API.
    raw_lines = loadStrings(lyrics_file);
    lyrics.add(new LyricPair(0, "[Stay tuned for scrolling lyrics]"));

    if (raw_lines == null) {
        // File not found or was otherwise inaccessible.
        lyrics.add(new LyricPair(0, "[Error loading LRC file " + lyrics_file + "]"));
        return;
    }

    // Iterate over every line of the LRC file.
    for (String line : raw_lines) {
        /* Lyrics are stored using the synchronized LRC format: see
         * https://en.wikipedia.org/wiki/LRC_(file_format)
         *
         * This uses regex to extract the relavant times and text of each line.
         * Field 1 = timestamps matching the line (there may be more than one).
         * Field 2 = the text. Each line looks something like: [01:32:48]Hello world.
         *
         * Regex (regular expression) matching is a very powerful tool in itself,
         * with specific syntaxes which I won't go into detail about here. See
         * https://en.wikipedia.org/wiki/Regular_expression has in-depth examples.
         */
        String[][] fields = matchAll(line, "((?:\\[\\d{2,}\\:\\d{2}\\.\\d{2,}\\])+)(.*)");
        if (fields != null) {
            for (String match[] : fields) {
                /* Now, for each field, process the timestamp part further to extract
                 * The time in milliseconds where each line should be shown.
                 */
                String ts_fields[][] = matchAll(match[1], "(\\d{2,})\\:(\\d{2})\\.(\\d{2,})");
                String text = match[2];

                // If the text string is empty, explicitly make it a space instead of null.
                // This prevents null pointer exceptions.
                if (text.isEmpty()) {
                    text = " ";
                }

                if (ts_fields != null) {
                    // If the time fields are valid, create a LyricPair object with the
                    // time (in milliseconds from 0:00) and text associated with it.
                    for (String[] ts_match : ts_fields) {
                        int minutes = int(ts_match[1]);
                        int seconds = int(ts_match[2]);
                        int milliseconds = int(ts_match[3]);
                        int total_milliseconds = (minutes * 60000) + (seconds * 1000) + milliseconds;

                        LyricPair lyric_pair = new LyricPair(total_milliseconds, text);
                        // Add the lyrics line to the list of lines, which will then be sorted.
                        lyrics.add(lyric_pair);

                        println("Adding lyrics line '" + text + "' at position " + total_milliseconds);
                    }
                }
            }
        }
    }

    // Sort our lyrics lines so that they show up in the right order.
    Collections.sort(lyrics);
}

void setup() {
    size(900, 600);
    background(250);
    loadLyrics(lyrics_file);

    surface.setTitle("Niceviz! Player");

    minim = new Minim(this);
    player = minim.loadFile(song_file);

    /* The player objects becomes null when an invalid file is loaded.
     * Checks like these are needed to prevent the app from crashing with a
     * NullPointerException.
     */
    if (player != null) {
        player.loop();  // Play the song in a loop
    }

    // Make the window resizable
    surface.setResizable(true);

    /* rectMode(CORNERS) interprets the first two parameters of rect()
     * as the location of one corner, and the third and fourth parameters
     * as the location of the opposite corner.
     */
    rectMode(CORNERS);

    frameRate(60);

    // Center all text both horizontally and vertically
    textAlign(CENTER, CENTER);

    // Choose a random color scheme to draw the bars.
    color_scheme = chooseRandomColor();

}

// Define our list of possible colour schemes
int[][][] colors = {
                    // Pink and salmon
                    {{255, 214, 221}, {250, 217, 210}},
                    // Light blue and sky blue
                    {{211, 211, 232}, {197, 219, 254}},
                    // Orange
                    {{255, 217, 135}, {232, 177, 232}},
                    // Light greens
                    {{182, 240, 163}, {212, 255, 133}},
                    // Gold and yellow
                    {{245, 225, 112}, {254, 248, 129}},
                    // Purples
                    {{233, 208, 245}, {176, 144, 209}},
                    // Greys
                    {{222, 222, 222}, {160, 160, 160}}
                 };

int[][] chooseRandomColor() {
    // Choose a random color scheme from the list of color schemes
    int rand = int(random(0, colors.length));
    return colors[rand];
}

void draw() {
    if (height <= 0 || width <= 0) {
        // If the window size is too small, abort attempts to draw instead of crashing
        exit();
    }

    if (player == null) {
        background(250);
        // Song file is invalid; make that clear to the user.

        fill(0);
        text("Invalid song file:\n" + song_file, width/2, height/2);

    // Save CPU by only drawing the screen if we're playing a song
    } else if (player.isPlaying()) {
        /* Update the lyric positions. If the current player position is greater or
         * equal to the time when the lyrics should change (stored in lyrics),
         * increment our position in the lyrics list (current_position) and move to the
         * next line of text.
         */
        try {
            lyric_pair = lyrics.get(current_position);
        } catch (IndexOutOfBoundsException e) {
            reached_end = true;
            println("setting reached_end");
        }

        next_position = lyric_pair.time;
        text = lyric_pair.text;
        println("Current player position in ms: " + player.position());
        println("Position to switch: " + next_position);
        if (player.position() >= next_position && !reached_end) {
            /* The player shows 3 lines at once, to give a sort of scrolling feel.
             * First, clear the list of lines to show. Then add
             * 1) the lyrics line before the current one,
             * 2) the current lyrics line,
             * and 3) the lyrics line after the current one,
             * to the list.
             *
             * If any of the before/after lines are missing, just ignore them
             * and show what we can.
             */
            shown_lines.clear();

            try {
                shown_lines.add(lyrics.get(current_position-1).text);
            } catch (IndexOutOfBoundsException e) {
                ; // Ignore out of bounds errors
            }

            shown_lines.add(text);

            try {
                shown_lines.add(lyrics.get(current_position+1).text);
            } catch (IndexOutOfBoundsException e) {
                ;
            }

            current_position += 1;
        } else if (reached_end && player.position() <= next_position) {
            /* Once we reach the end of the song, and the player position
             * has wrapped back to the start we should reset the lyrics counter too.
             */
            reached_end = false;
            current_position = 0;
        }
        level = player.mix.level(); // Get the mix levels of the player

        if (random(1) > .99) {
            // Switch to a different colour scheme every once in a while.
            color_scheme = chooseRandomColor();
        }

        /* The bars visualization this program shows is really just a combination of
         * boxes drawn, relative to the current sound level and the window height.
         * This rectsize value derived from the audio level, but with a hard limit of
         * somewhere between 0 and 0.02 (so the bars are never gone completely)
         * As the player progresses, the bars will draw all over the window and fill it
         * with trails of pretty colours.
         */
        float rectsize = max(random(0, 0.02), level);
        stroke(0, 40);  // Partly translucent outline for each box for a blurred feel
        strokeWeight(1);

        /* I wish there was a better way to do this. Each colour scheme is a list of
         * (r, g, b) values, so fill() must be given the values for each colour.
         * I truly wish there was a more efficient way to do this...
         * Also, opacity is 12% to give the boxes a nice trailing colour.
         */
        fill(color_scheme[0][0], color_scheme[0][1], color_scheme[0][2], 12);

        /* All rectangles are drawn relative to the window width and height.
         * The maximum size it can be, however, is 100% of the window height.
         */
        rect(width, min(height, height*rectsize), 0, height);

        /* The rest are the same, with different colours and a larger rectangle size
         * (multiplied by an offset).
         */
        fill(color_scheme[1][0], color_scheme[1][1], color_scheme[1][2], 12);
        rect(width, min(height, height*rectsize*1.8), 0, height);

        fill(255, 100); // Higher opacity for the white area
        rect(width, min(height, height*rectsize*3), 0, height);

        // Draw some buttons for choosing files
        fill(200);
        stroke(128);
        strokeWeight(3); // Use a hicker button outline
        choose_file_coords = new float[]{width*0.85, height*0.02, width*0.99, height*0.1};
        rect(width*0.85, height*0.02, width*0.99, height*0.1);
        fill(1);

        textSize(int(height/32));
        text("Choose File", width*0.92, height*0.06);

        // Reset text size back to the bigger version
        fill(0);
        textSize(int(height/24));

        if (show_text) {
            if (shown_lines != null) {
                // Join all the lyrics lines to show with a newline between each one.
                // Display this text in the centre of the window.
                text(String.join("\n", shown_lines), width/2, height/2);
            }
            text("Left click to toggle text, right click to pause/play.", width/2, height*0.9);
        }
    }
}

void fileSelected(File selection) {
    // This implements the file selection receiver.
    if (selection != null) { // If the selection exists:
        // Get the song filename
        song_file = selection.getAbsolutePath();
        println("New song file: " + song_file);

        /* Derive the lyrics filename from that. Split the given file
         * by a ".", and find the corresponding .lrc file by replacing
         * the extension (e.g. "mp3") with "lrc".
         */
        String file_ext[] = split(song_file, '.');

        // There was no file extension on the file given
        if (file_ext.length < 2) {
            print("Unknown file type: " + song_file);
            player.pause();
            return;
        } else {
            file_ext[file_ext.length-1] = "lrc";

            // Join the string back together.
            lyrics_file = join(file_ext, ".");

            setup(); // Re-run setup() to reload lyrics & reset the player
        }
    } else {
        /* The user clicked cancel or close in the file
         * chooser, so nothing was selected. Just resume
         * the last song, if applicable.
         */
        if (player != null) {
            player.loop();
        }
    }
}

void mousePressed() {
    if (mouseButton == LEFT) {
        // If we're pressing the "Choose file" button, then handle that separately

        if (choose_file_coords != null && choose_file_coords[0] <= mouseX && mouseX <= choose_file_coords[2] &&
                (choose_file_coords[1] <= mouseY && mouseY <= choose_file_coords[3])) {
            selectInput("Select an audio file to read:", "fileSelected");

            if (player != null) {
                player.pause();
            }

        } else { // Left click elsewhere toggles the lyrics display
            show_text = !show_text;
            println("showtext: " + show_text);
        }
    } else if (player != null) {
        // Right click toggles pause/play, if there is a valid file in the player.
        if (player.isPlaying()) {
            player.pause();
        } else {
            player.loop();
        }
    }
}

void mouseWheel(MouseEvent event) {
    /* Hidden bonus: you can use the scroll wheel to seek forward! I decided not
     * to implement scrolling backwards, since it caused awful choppiness in the
     * Minim player.
     */
    if (player != null) {
        int amount = abs(int(event.getCount()*1000));
        player.skip(amount);
    }
}