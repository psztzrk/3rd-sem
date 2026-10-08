public class Point {
    double x;
    double y;

    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public Point(String[] args, int idx) {
        this(Double.parseDouble(args[idx]), Double.parseDouble(args[idx + 1]));
    }

    public void print() {
        IO.println("At (%2.1f, %2.1f)".formatted(x, y));
    }

    public void print(String text, Point point) {
        IO.println("At (%2.1f, %2.1f) %s (%2.1f, %2.1f)"
                .formatted(x, y, text, point.x, point.y));
    }

    public void shift(double dx, double dy) {
        x += dx;
        y += dy;
    }

    public void mirror(double cx, double cy) {
        x = 2 * cx - x;
        y = 2 * cy - y;
    }

    public double distance(Point point) {
        double dx = x - point.x;
        double dy = y - point.y;
        return Math.sqrt(dx * dx + dy * dy);
    }
}