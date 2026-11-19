package view;

import model.ColorClickerModel;

import javax.swing.*;
import java.awt.*;
import java.util.Optional;

public class ColorClickerGUI {
    // TODO: add a constant for the leaderboard size (top 10 runs)
    private JFrame frame;
    private ColorClickerModel model;
    // TODO: add a field for the repository from your persistence layer
    private BoardPanel boardPanel;
    private JLabel timerLabel;
    private Timer timer;
    private long startTime;

    // TODO: take the repository as a second constructor parameter and store it in the field
    public ColorClickerGUI(ColorClickerModel model) {
        this.model = model;

        this.frame = new JFrame("ColorClicker");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JMenuBar menuBar = new JMenuBar();
        JMenu newGameMenu = new JMenu("New Game");
        int[] boardSizes = new int[]{5, 10, 15, 20};
        for (int boardSize : boardSizes) {
            JMenuItem menuItem = new JMenuItem(boardSize + " x " + boardSize);
            menuItem.addActionListener((e) -> newGame(boardSize));
            newGameMenu.add(menuItem);
        }
        menuBar.add(newGameMenu);
        frame.setJMenuBar(menuBar);

        this.boardPanel = new BoardPanel(this.model, this::checkGameOver);
        frame.add(boardPanel, BorderLayout.CENTER);

        this.timerLabel = new JLabel();
        frame.add(timerLabel, BorderLayout.SOUTH);
        this.timer = new Timer(100, (e) -> updateTimerLabel());
        restartTimer();

        frame.pack();
        frame.setVisible(true);
    }

    private void newGame(int boardSize) {
        model.initializeBoard(boardSize);
        refreshView();
        restartTimer();
    }

    private void checkGameOver() {
        if (!model.isGameOver()) {
            return;
        }
        timer.stop();
        long elapsedMillis = System.currentTimeMillis() - startTime;
        int choice = JOptionPane.showConfirmDialog(frame,
                "Game over! Time: " + formatElapsed() + "\nDo you want to save this run?",
                "Game Over",
                JOptionPane.YES_NO_OPTION,
                JOptionPane.INFORMATION_MESSAGE);
        if (choice == JOptionPane.YES_OPTION) {
            promptPlayerName().ifPresent(name ->
                    saveRun(name, model.getBoardSize(), model.getClickNumber(), elapsedMillis));
        }
        newGame(model.getBoardSize());
    }

    /**
     * Asks for the player's name until a non-blank one is given.
     * Returns empty if the user cancels or closes the dialog.
     */
    private Optional<String> promptPlayerName() {
        while (true) {
            String input = JOptionPane.showInputDialog(frame,
                    "Enter your name:",
                    "Save Run",
                    JOptionPane.QUESTION_MESSAGE);
            if (input == null) {
                return Optional.empty();
            }
            String name = input.trim();
            if (!name.isEmpty()) {
                return Optional.of(name);
            }
            JOptionPane.showMessageDialog(frame,
                    "The name cannot be empty.",
                    "Invalid Name",
                    JOptionPane.WARNING_MESSAGE);
        }
    }

    private void saveRun(String playerName, int boardSize, int clicks, long elapsedMillis) {
        // TODO: persist the run into the SQLite database through the repository
        // TODO: if saving fails (SQLException), show an error dialog and return
        // TODO: if saving succeeds, show the leaderboard for this board size
    }

    private void showLeaderboard(int boardSize) {
        // TODO: load the top 10 runs for this board size from the repository
        // TODO: if loading fails (SQLException), show an error dialog and return
        // TODO: show the runs (rank, name, time, clicks) in a read-only JTable inside a JOptionPane
    }

    private void restartTimer() {
        startTime = System.currentTimeMillis();
        updateTimerLabel();
        timer.restart();
    }

    private void updateTimerLabel() {
        timerLabel.setText("Time: " + formatElapsed());
    }

    // TODO: move the formatting into a formatMillis(long) helper so the leaderboard can reuse it
    private String formatElapsed() {
        long elapsed = System.currentTimeMillis() - startTime;
        return String.format("%d.%d s", elapsed / 1000, (elapsed % 1000) / 100);
    }

    private void refreshView() {
        boardPanel.rebuild();
        frame.pack();
    }
}
