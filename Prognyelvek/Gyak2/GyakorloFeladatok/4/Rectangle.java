public class Rectangle {
    double x;
    double y;
    double width;
    double height;

    public Rectangle(double x, double y, double width, double height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }

    public Point topLeft() {
        return new Point(Math.min(x, x + width), Math.max(y, y + height));
    }

    public Point topRight() {
        return new Point(Math.max(x, x + width), Math.max(y, y + height));
    }

    public Point bottomLeft() {
        return new Point(Math.min(x, x + width), Math.min(y, y + height));
    }

    public Point bottomRight() {
        return new Point(Math.max(x, x + width), Math.min(y, y + height));
    }
}