package model;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.Random;

public class ColorClickerModel {
    private static final int NUMBER_OF_EXTRA_TILES_TO_COLOR = 4;
    private final Random rng = new Random();

    private Tile[][] board;
    private int boardSize;
    private int clickNumber = 0;

    public void initializeBoard(int size) {
        this.boardSize = size;
        this.clickNumber = 0;
        this.board = new Tile[size][size];
        for (int i = 0; i < this.boardSize; ++i) {
            for (int j = 0; j < this.boardSize; ++j) {
                board[i][j] = new Tile();
            }
        }
    }

    public int getBoardSize() {
        return this.boardSize;
    }

    public int getClickNumber() {
        return this.clickNumber;
    }

    public void clickTile(Tile tile) {
        if (tile.isColoured()) {
            return;
        }
        this.clickNumber++;
        TileColor color = getRandomColor();
        tile.setColor(color);
        tile.setClickNumber(this.clickNumber);

        List<Tile> uncolouredTiles = new ArrayList<>();
        for (Tile[] row : board) {
            for (Tile t : row) {
                if (!t.isColoured()) {
                    uncolouredTiles.add(t);
                }
            }
        }
        Collections.shuffle(uncolouredTiles, rng);
        int count = Math.min(NUMBER_OF_EXTRA_TILES_TO_COLOR, uncolouredTiles.size());
        for (int i = 0; i < count; ++i) {
            uncolouredTiles.get(i).setColor(color);
            uncolouredTiles.get(i).setClickNumber(this.clickNumber);
        }
    }

    private TileColor getRandomColor() {
        TileColor[] colors = TileColor.values();
        return colors[this.rng.nextInt(colors.length)];
    }

    public boolean isGameOver() {
        if (this.board == null) {
            return false;
        }
        for (Tile[] row : board) {
            for (Tile t : row) {
                if (!t.isColoured()) {
                    return false;
                }
            }
        }
        return true;
    }

    public Optional<Tile[][]> getBoard() {
        if (this.board == null) {
            return Optional.empty();
        } else {
            return Optional.of(this.board);
        }
    }
}
