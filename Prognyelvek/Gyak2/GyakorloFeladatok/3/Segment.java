public class Segment {
    private static final double EPSILON = 1e-9;

    double x1;
    double y1;
    double x2;
    double y2;

    public Segment(double x1, double y1, double x2, double y2) {
        if (Math.abs(x1 - x2) < EPSILON && Math.abs(y1 - y2) < EPSILON) {
            throw new IllegalArgumentException("A segment must have two different endpoints.");
        }
        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;
    }

    public Line line() {
        double a = y2 - y1;
        double b = x1 - x2;
        double c = a * x1 + b * y1;
        return new Line(a, b, c);
    }

    public boolean contains(Point point) {
        return Math.abs(orientation(point)) < EPSILON
                && point.x >= Math.min(x1, x2) - EPSILON
                && point.x <= Math.max(x1, x2) + EPSILON
                && point.y >= Math.min(y1, y2) - EPSILON
                && point.y <= Math.max(y1, y2) + EPSILON;
    }

    public double orientation(Point point) {
        return (y2 - y1) * (point.x - x2) - (point.y - y2) * (x2 - x1);
    }

    public boolean intersects(Segment segment) {
        Point firstStart = new Point(x1, y1);
        Point firstEnd = new Point(x2, y2);
        Point secondStart = new Point(segment.x1, segment.y1);
        Point secondEnd = new Point(segment.x2, segment.y2);

        double o1 = orientation(secondStart);
        double o2 = orientation(secondEnd);
        double o3 = segment.orientation(firstStart);
        double o4 = segment.orientation(firstEnd);

        if (oppositeSigns(o1, o2) && oppositeSigns(o3, o4)) {
            return true;
        }

        return Math.abs(o1) < EPSILON && contains(secondStart)
                || Math.abs(o2) < EPSILON && contains(secondEnd)
                || Math.abs(o3) < EPSILON && segment.contains(firstStart)
                || Math.abs(o4) < EPSILON && segment.contains(firstEnd);
    }

    private static boolean oppositeSigns(double first, double second) {
        return first > EPSILON && second < -EPSILON
                || first < -EPSILON && second > EPSILON;
    }
}