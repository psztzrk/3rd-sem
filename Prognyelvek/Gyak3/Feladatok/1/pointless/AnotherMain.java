package pointless;

import point2d.Point;

public class AnotherMain {
    public static void main(String... args) {
        point2d.Point fullyQualifiedPoint = new point2d.Point(10.0, 20.0);
        Point importedPoint = new Point(1.2, -3.4);
        fullyQualifiedPoint.print();
        importedPoint.print();
    }
}