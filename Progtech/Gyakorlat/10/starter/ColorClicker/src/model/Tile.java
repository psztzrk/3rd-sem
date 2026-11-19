package model;

public class Tile
{
    private TileColor color;
    private int clickNumber;

    public TileColor getColor() {
        return this.color;
    }
    public void setColor(TileColor color) {
        this.color = color;
    }

    public int getClickNumber() {
        return clickNumber;
    }

    public void setClickNumber(int clickNumber) {
        this.clickNumber = clickNumber;
    }

    public boolean isColoured() {
        return this.color != null;
    }
}
