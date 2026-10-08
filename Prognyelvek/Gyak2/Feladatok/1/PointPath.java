import java.util.Locale;

public class PointPath {
    public static void main(String... args) {
        Locale.setDefault(Locale.of("hu"));

        if (args.length < 4 || args.length % 2 != 0) {
            throw new IllegalArgumentException("Provide at least two points.");
        }

        Point previous = new Point(args, 0);
        previous.print();
        double totalDistance = 0.0;

        for (int idx = 2; idx < args.length; idx += 2) {
            Point current = new Point(args, idx);
            double distance = previous.distance(current);
            totalDistance += distance;
            current.print(
                    "with a total distance of %2.1f and a distance of %2.1f from"
                            .formatted(totalDistance, distance),
                    current);
            previous = current;
        }
    }
}