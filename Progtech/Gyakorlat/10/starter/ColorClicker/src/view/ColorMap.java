package view;

import model.TileColor;

import java.awt.*;

final class ColorMap {
    private ColorMap() {
    }

    static Color toAwtColor(TileColor tileColor) {
        return switch (tileColor) {
            case RED -> Color.RED;
            case GREEN -> Color.GREEN;
            case BLUE -> Color.BLUE;
            case YELLOW -> Color.YELLOW;
        };
    }
}
