package plane.but.not.flying;

import plane.Circle;
import plane.PublicCircle;

public class CircleMain {
    public static void main(String... args) {
        PublicCircle publicCircle = new PublicCircle();
        IO.println(publicCircle.getArea());
        publicCircle.x = 5.0;
        publicCircle.y = 2.0;
        publicCircle.radius = 10.0;
        IO.println(publicCircle.getArea());

        Circle circle = new Circle(0.0, 0.0, 1.0);
        IO.println(circle.getArea());
        circle.setX(5.0);
        circle.setY(2.0);
        circle.setRadius(10.0);
        IO.println(circle.getArea());

        if (args.length > 0) {
            circle.setRadius(Double.parseDouble(args[0]));
            IO.println(circle.getArea());
        }
    }
}