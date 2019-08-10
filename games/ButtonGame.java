/*
The classic Chase The Button game.
 */

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.Random;

public class ButtonGame {
    public static int DEFAULT_WIDTH = 600;
    public static int DEFAULT_HEIGHT = 400;
    public static int BUTTON_WIDTH = 100;
    public static int BUTTON_HEIGHT = 50;
    public static int MAX_DELAY = 250;

    private int windowWidth = DEFAULT_WIDTH;
    private int windowHeight = DEFAULT_HEIGHT;

    private JFrame frame;
    private JButton button;
    private JLabel label;
    private Random random;
    private int pressedTimes = 0;

    public ButtonGame() {
        frame = new JFrame();
        frame.setTitle("BUTTON GAME");
        frame.setSize(DEFAULT_WIDTH, DEFAULT_HEIGHT);
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        button = new JButton();
        button.setActionCommand("pressed");
        button.addActionListener(actionEvent -> {
            if (actionEvent.getActionCommand().equals("pressed")) {
                pressedTimes++;
                moveButton();
            }
        });
        button.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseEntered(MouseEvent mouseEvent) {
                if (mouseEvent.getSource() == button) {
                    Timer timer = new Timer(random.nextInt(MAX_DELAY), actionEvent -> moveButton());
                    timer.setRepeats(false);
                    timer.start();
                }
            }
        });
        button.setFocusable(false); //no cheating!!!
        button.setText("Click me!");
        button.setSize(BUTTON_WIDTH, BUTTON_HEIGHT);

        label = new JLabel();
        label.setHorizontalAlignment(SwingConstants.CENTER);

        frame.add(label);
        frame.add(button);
        frame.addComponentListener(new ComponentAdapter() {
            @Override
            public void componentResized(ComponentEvent componentEvent) {
                Dimension bounds = frame.getBounds().getSize();
                windowWidth = (int) bounds.getWidth();
                windowHeight = (int) bounds.getHeight();
                resizeElements();
            }
        });

        random = new Random();
    }

    private void resizeElements() {
        label.setBounds(0, 0, windowWidth, (int)(windowHeight * 0.25));
        moveButton();
    }

    public void start() {
        moveButton();
        frame.setVisible(true);
    }

    public void moveButton() {
        label.setText("You've pressed the button " + Integer.toString(pressedTimes) + " time(s).");
        button.setBounds(random.nextInt(windowWidth -2*BUTTON_WIDTH),
                         random.nextInt(windowHeight -2*BUTTON_HEIGHT),
                         BUTTON_WIDTH, BUTTON_HEIGHT);
    }

    public static void main(String[] args) {
        ButtonGame app = new ButtonGame();
        app.start();
    }
}

