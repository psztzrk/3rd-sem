import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class BlackHole {
    int boardWidth = 600;
    int boardHeight = 650;

    JFrame frame = new JFrame("Blackhole game");
    JLabel textLabel = new JLabel();
    JPanel textPanel = new JPanel();
    JPanel boardPanel = new JPanel();
    JButton[] menu = new JButton[3];  // game starter 3 board size choice

    JButton[] board5By5 = new JButton[25];  // 5x5
    JButton[] board7By7 = new JButton[42];  // 7x7
    JButton[] board9Bx9 = new JButton[81];  // 9x9

    ImageIcon blueRocket;
    ImageIcon greyRocket;

    BlackHole() {

        frame.setSize(boardWidth, boardHeight);
        frame.setLocationRelativeTo(null);
        frame.setResizable(false);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame. setLayout(new BorderLayout());

        textLabel.setFont(new Font("Arial", Font.PLAIN, 50));
        textLabel.setHorizontalAlignment(JLabel.CENTER);
        textLabel.setText("valami lesz majd - talán...");
        textLabel.setOpaque(true);

        textPanel.setLayout((new BorderLayout()));
        textPanel.add(textLabel);
        frame.add(textPanel, BorderLayout.NORTH);

        boardPanel.setLayout(new GridLayout(5,5));
        boardPanel.setBackground(Color.BLACK);
        frame.add(boardPanel);
        Image blueImg = new ImageIcon(getClass().getResource("./bluerocket.png")).getImage();
        Image greyImg = new ImageIcon(getClass().getResource("./greyrocket.png")).getImage();
        blueRocket = new ImageIcon(blueImg.getScaledInstance(110, 110, Image.SCALE_SMOOTH));
        greyRocket = new ImageIcon(greyImg.getScaledInstance(110, 110, Image.SCALE_SMOOTH));

        for (int i = 0; i < 25; i++) {
            JButton tile = new JButton();
            board5By5[i] = tile;
            boardPanel.add(tile);

            tile.setIcon(greyRocket);
        }

        //redIcon = new ImageIcon(getClass().getResource("./red-dot.png"));
        //blueIcon = new ImageIcon(getClass().getResource("./blue-dot.png"));

        frame.setVisible(true);
    }
}
