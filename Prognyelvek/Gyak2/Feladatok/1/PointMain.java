import java.util.Locale;

public class PointMain {
    private static final double END_INDICATOR = -123456;

    public static void main(String... args) {
        Locale.setDefault(Locale.of("hu"));

        boolean readFromInput = args.length == 2;
        if (args.length == 0) {
            args = "10.0 20.0 1.2 -3.4 10.0 10.0".split(" ");
        }

        if (args.length < 2) {
            throw new IllegalArgumentException("The starting point requires two coordinates.");
        }
        if (!readFromInput && args.length % 2 != 0) {
            throw new IllegalArgumentException("Coordinates must be provided in pairs.");
        }

        Point point = new Point(args, 0);
        point.print();

        int argumentIndex = 2;
        int step = 1;
        while (readFromInput || argumentIndex + 1 < args.length) {
            boolean shifting = step % 2 == 1;
            int pointNumber = (step + 1) / 2;
            Point next = getNextPoint(args, argumentIndex, readFromInput, shifting, pointNumber);

            if (next.x == END_INDICATOR) {
                IO.println("Special input encountered, exiting");
                return;
            }

            if (shifting) {
                point.shift(next.x, next.y);
                point.print("at step #%d after being shifted by".formatted(step), next);
            } else {
                point.mirror(next.x, next.y);
                point.print("at step #%d after being mirrored on".formatted(step), next);
            }

            argumentIndex += 2;
            step++;
        }
    }

    private static Point getNextPoint(
            String[] args,
            int idx,
            boolean readFromInput,
            boolean shifting,
            int pointNumber) {
        if (!readFromInput && idx + 1 < args.length) {
            return new Point(args, idx);
        }

        String operation = shifting ? "shifting" : "mirroring";
        double x = Double.parseDouble(
                IO.readln("Input x for %s Point#%d: ".formatted(operation, pointNumber)));
        double y = Double.parseDouble(
                IO.readln("Input y for %s Point#%d: ".formatted(operation, pointNumber)));
        return new Point(x, y);
    }
}