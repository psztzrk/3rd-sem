package view;

import model.Game;
import model.Board;
import model.CellType;
import model.Direction;
import model.MoveResult;

import java.awt.*;
import javax.swing.*;

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
    private int selectedRow = -1;
    private int selectedCol = -1;

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

        // valaszto legordulo menu
        JPanel menuPanel = new JPanel();
        JLabel sizeLabel = new JLabel("Board size:");
        sizeSelector = new JComboBox<>(new Integer[]{5, 7, 9});
        JButton startButton = new JButton("New game");
        textLabel.setHorizontalAlignment(JLabel.CENTER);
        statusLabel = new JLabel("Start a new game!");

        menuPanel.add(statusLabel);
        menuPanel.add(sizeLabel);
        menuPanel.add(sizeSelector);
        menuPanel.add(startButton);

        frame.add(menuPanel, BorderLayout.NORTH);

        // start button actionkezelo
        startButton.addActionListener(e -> {
            int selectedSize = (int) sizeSelector.getSelectedItem();
            createBoard(selectedSize);
        });

        // tabla
        boardPanel = new JPanel();
        frame.add(boardPanel, BorderLayout.CENTER);

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

        upButton.addActionListener(e -> moveSelectedShip(Direction.UP));
        downButton.addActionListener(e -> moveSelectedShip(Direction.DOWN));
        leftButton.addActionListener(e -> moveSelectedShip(Direction.LEFT));
        rightButton.addActionListener(e -> moveSelectedShip(Direction.RIGHT));

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
            for (int col = 0; col < size; col++) {
                JButton tile = new JButton();
                tile.setBorder(BorderFactory.createLineBorder(Color.GRAY));
                board[row][col] = tile;
                final int r = row;
                final int c = col;

                tile.addActionListener(e -> selectCell(r, c));

                boardPanel.add(tile);
            }
        }

        statusLabel.setText("New" + size + "x" + size + "game!");

        // frissites
        updateBoard();

        boardPanel.revalidate();
        boardPanel.repaint();

        frame.revalidate();
        frame.repaint();

        statusLabel.setText("Blue player's turn!");

    }

    private void updateBoard(){
        for (int row = 0; row < game.getBoard().getSize(); row++) {
            for (int col = 0; col < game.getBoard().getSize(); col++) {

                CellType cell = game.getBoard().getCell(row, col);
                JButton tile = board[row][col];

                tile.setText("");
                tile.setIcon(null);
                tile.setBackground(Color.WHITE);

                switch (cell) {
                    case CellType.EMPTY:
                        tile.setText("");
                        break;
                    case CellType.GREY_SHIP:
                        Image greyImg = new ImageIcon(getClass().getResource("/resources/greyrocket.png")).getImage();
                        greyRocket = new ImageIcon(greyImg.getScaledInstance(70, 70, Image.SCALE_SMOOTH));
                        tile.setIcon(greyRocket);
                        break;
                    case CellType.BLUE_SHIP:
                        Image blueImg = new ImageIcon(getClass().getResource("/resources/bluerocket.png")).getImage();
                        blueRocket = new ImageIcon(blueImg.getScaledInstance(70, 70, Image.SCALE_SMOOTH));
                        tile.setIcon(blueRocket);
                        break;
                    case CellType.BLACK_HOLE:
                        Image holeImg = new ImageIcon(getClass().getResource("/resources/blackhole.png")).getImage();
                        blackHole = new ImageIcon(holeImg.getScaledInstance(70, 70, Image.SCALE_SMOOTH));
                        tile.setIcon(blackHole);
                        break;
                }
            }
        }
    }

    private  void selectCell(int row, int col){
        CellType cell = game.getBoard().getCell(row, col);

        if (cell == CellType.GREY_SHIP || cell == CellType.BLUE_SHIP){
            selectedRow = row;
            selectedCol = col;

            updateBoard();

            board[row][col].setBackground(Color.GREEN);
        }
    }

    private void moveSelectedShip(Direction direction) {

        // Ha nincs kiválasztott hajó
        if (selectedRow == -1 || selectedCol == -1) {
            JOptionPane.showMessageDialog(frame,
                    "Select a ship first!");
            return;
        }

        MoveResult result = game.makeMove(
                selectedRow, selectedCol, direction);

        if (result == MoveResult.BLOCKED) {
            JOptionPane.showMessageDialog(frame,
                    "The ship cannot move in this direction!");
        }

        if (result == MoveResult.ABSORBED) {
            JOptionPane.showMessageDialog(frame,
                    "The ship was absorbed by the black hole!");

            selectedRow = -1;
            selectedCol = -1;
        }

        if (result == MoveResult.MOVED) {
            // Megkeressük, hol van most a hajó
            selectedRow = -1;
            selectedCol = -1;
        }

        if (game.gameOver()) {

            CellType winner = game.getWinner();

            String winnerName = winner == CellType.BLUE_SHIP
                    ? "Blue"
                    : "Grey";

            JOptionPane.showMessageDialog(frame,
                    winnerName + " player wins!");

            statusLabel.setText(winnerName + " wins!");

            createBoard(5);
            return;
        }

        updateBoard();

        statusLabel.setText("Current player: " +
                (game.getCurrentPlayer() == CellType.BLUE_SHIP
                        ? "Blue"
                        : "Grey"));


    }


}

