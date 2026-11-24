import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

public class GameWindow {

    private JFrame frame;
    private int boardWidth = 700;
    private int boardHeight = 750;
    private int size = 5;
    private String turner;
    ImageIcon blueRocket;
    ImageIcon greyRocket;
    ImageIcon blackHole;
    JLabel textLabel = new JLabel();
    JPanel textPanel = new JPanel();
    JPanel boardPanel = new JPanel();
    JButton[][] board;
    private Game game;
    private JComboBox<Integer> sizeSelector;
    private JLabel statusLabel;

    public GameWindow(){
        createWindow();
    }

    private void createWindow(){

        //maga az ablak
        frame = new JFrame("Blackhole game");
        frame.setSize(boardWidth, boardHeight);
        frame.setLocationRelativeTo(null);
        frame.setResizable(false);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());

        // felso text
        JPanel topPanel = new JPanel(new BorderLayout());

        textLabel.setFont(new Font("Arial", Font.PLAIN, 40));
        textLabel.setHorizontalAlignment(JLabel.CENTER);
        textLabel.setText("The Blackhole game!");
        //textLabel.setOpaque(true);
        topPanel.add(textLabel, BorderLayout.NORTH);

        // valaszto legordulo menu
        JPanel menuPanel = new JPanel();

        JLabel sizeLabel = new JLabel("Board size:");
        sizeSelector = new JComboBox<>(new Integer[]{5, 7, 9});
        JButton startButton = new JButton("New game");

        statusLabel = new JLabel("Start a new game!");

        menuPanel.add(statusLabel);
        menuPanel.add(sizeLabel);
        menuPanel.add(sizeSelector);
        menuPanel.add(startButton);

        topPanel.add(menuPanel, BorderLayout.NORTH);

        frame.add(topPanel, BorderLayout.NORTH);

        //iranyitos gombok
        JPanel controlPanel = new JPanel();

        JButton upButton = new JButton("UP");
        JButton downButton = new JButton("DOWN");
        JButton leftButton = new JButton("LEFT");
        JButton rightButton = new JButton("RIGHT");

        controlPanel.add(upButton);
        controlPanel.add(downButton);
        controlPanel.add(leftButton);
        controlPanel.add(rightButton);

        frame.add(controlPanel, BorderLayout.SOUTH);
        frame.add(boardPanel, BorderLayout.CENTER);
        // start button
        startButton.addActionListener(e -> {
            int selectedSize = (int) sizeSelector.getSelectedItem();
            createBoard(selectedSize);
        });

        //TODO actionlisteners

        createBoard(size);
        frame.setVisible(true);
    }

    private void createBoard(int size){
        boardPanel.removeAll();

        //uj jatek
        game = new Game(size);
        Board gameBoard = game.getBoard();

        // gombok
        board = new JButton[size][size];

        boardPanel.setLayout(new GridLayout(size, size));
        boardPanel.setBackground(Color.BLACK);
        for (int row = 0; row < size; row++)
        {
            for (int col = 0; col < size; col++)
            {
                JButton tile = new JButton();
                tile.setFocusable(false);
                tile.setBorder(BorderFactory.createLineBorder(Color.GRAY));
                board[row][col] = tile;
                tile.setFocusable(false);

                CellType cell = gameBoard.getCells(row, col);

                switch (cell) {
                    case EMPTY:
                        tile.setText("");
                        break;
                    case GREY_SHIP:
                        Image greyImg = new ImageIcon(getClass().getResource("./greyrocket.png")).getImage();
                        greyRocket = new ImageIcon(greyImg.getScaledInstance(70, 70, Image.SCALE_SMOOTH));
                        tile.setIcon(greyRocket);
                        break;
                    case BLUE_SHIP:
                        Image blueImg = new ImageIcon(getClass().getResource("./bluerocket.png")).getImage();
                        blueRocket = new ImageIcon(blueImg.getScaledInstance(70, 70, Image.SCALE_SMOOTH));
                        tile.setIcon(blueRocket);
                        break;
                    case BLACK_HOLE:
                        Image holeImg = new ImageIcon(getClass().getResource("./blackhole.png")).getImage();
                        blackHole = new ImageIcon(holeImg.getScaledInstance(70, 70, Image.SCALE_SMOOTH));
                        tile.setIcon(blackHole);
                        break;
                }
                boardPanel.add(tile);
            }
        }

        statusLabel.setText("New" + size + "x" + size + "game!");

        // frissites
        boardPanel.revalidate();
        boardPanel.repaint();

        frame.revalidate();
        frame.repaint();

    }




}
