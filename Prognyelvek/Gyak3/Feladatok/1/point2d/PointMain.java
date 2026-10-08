package point2d;

import java.util.Locale;

public class PointMain {
    public static void main(String... args) {
        Locale.setDefault(Locale.of("en"));
        Point point = new Point(10.0, 20.0);
        point.print();

        Point shift = new Point(1.2, -3.4);
        point.shift(1.2, -3.4);
        point.print("after being shifted by", shift);
    }
}