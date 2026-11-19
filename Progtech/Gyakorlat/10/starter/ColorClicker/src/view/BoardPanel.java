package view;

import model.ColorClickerModel;
import model.Tile;

import javax.swing.*;
import java.awt.*;

class BoardPanel extends JPanel {
    private final ColorClickerModel model;
    private final Runnable onTileClicked;
    private JButton[][] tileButtons = new JButton[0][0];

    public BoardPanel(ColorClickerModel model, Runnable onTileClicked) {
        this.model = model;
        this.onTileClicked = onTileClicked;
        rebuild();
    }

    void rebuild() {
        this.removeAll();
        int size = model.getBoardSize();
        setLayout(new GridLayout(size, size));
        tileButtons = new JButton[size][size];
        for (int row = 0; row < size; row++) {
            for (int col = 0; col < size; col++) {
                JButton button = new JButton();
                button.setPreferredSize(new Dimension(60, 40));
                button.setForeground(Color.BLACK);
                tileButtons[row][col] = button;
                final int r = row;
                final int c = col;
                button.addActionListener((e) -> model.getBoard().ifPresent(board -> {
                    model.clickTile(board[r][c]);
                    refresh();
                    onTileClicked.run();
                }));
                add(button);
            }
        }
        refresh();
        revalidate();
        repaint();
    }

    void refresh() {
        model.getBoard().ifPresent(board -> {
            for (int row = 0; row < tileButtons.length; row++) {
                for (int col = 0; col < tileButtons[row].length; col++) {
                    Tile tile = board[row][col];
                    JButton button = tileButtons[row][col];
                    if (tile.isColoured()) {
                        button.setBackground(ColorMap.toAwtColor(tile.getColor()));
                        button.setText(String.valueOf(tile.getClickNumber()));
                    } else {
                        button.setBackground(null);
                        button.setText("");
                    }
                }
            }
        });
    }
}
