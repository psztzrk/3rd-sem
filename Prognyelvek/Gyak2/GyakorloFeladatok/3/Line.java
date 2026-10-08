public class Line {
    private static final double EPSILON = 1e-9;

    double a;
    double b;
    double c;

    public Line(double a, double b, double c) {
        if (Math.abs(a) < EPSILON && Math.abs(b) < EPSILON) {
            throw new IllegalArgumentException("At least one coefficient must be nonzero.");
        }
        this.a = a;
        this.b = b;
        this.c = c;
    }

    public boolean contains(Point point) {
        return Math.abs(a * point.x + b * point.y - c) < EPSILON;
    }

    public boolean isParallelWith(Line line) {
        return Math.abs(a * line.b - line.a * b) < EPSILON;
    }

    public boolean isOrthogonalTo(Line line) {
        return Math.abs(a * line.a + b * line.b) < EPSILON;
    }
}