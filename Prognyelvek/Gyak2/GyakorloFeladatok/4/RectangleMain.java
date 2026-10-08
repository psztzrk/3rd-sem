import java.util.Locale;

public class RectangleMain {
    public static void main(String... args) {
        Locale.setDefault(Locale.of("en"));

        if (args.length < 4 || args.length % 4 != 0) {
            throw new IllegalArgumentException("Provide one or more rectangles as groups of four values.");
        }

        Rectangle first = rectangleFrom(args, 0);
        double minX = first.bottomLeft().x;
        double minY = first.bottomLeft().y;
        double maxX = first.topRight().x;
        double maxY = first.topRight().y;

        for (int idx = 4; idx < args.length; idx += 4) {
            Rectangle rectangle = rectangleFrom(args, idx);
            minX = Double.min(minX, rectangle.bottomLeft().x);
            minY = Double.min(minY, rectangle.bottomLeft().y);
            maxX = Double.max(maxX, rectangle.topRight().x);
            maxY = Double.max(maxY, rectangle.topRight().y);
        }

        IO.println("Bounding rectangle: %2.1f;%2.1f - %2.1f;%2.1f"
                .formatted(minX, minY, maxX, maxY));
    }

    private static Rectangle rectangleFrom(String[] args, int idx) {
        return new Rectangle(
                Double.parseDouble(args[idx]),
                Double.parseDouble(args[idx + 1]),
                Double.parseDouble(args[idx + 2]),
                Double.parseDouble(args[idx + 3]));
    }
}