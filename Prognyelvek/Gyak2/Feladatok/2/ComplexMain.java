import java.util.Locale;

public class ComplexMain {
    public static void main(String... args) {
        Locale.setDefault(Locale.of("hu"));

        Complex number = new Complex(4.0, 2.0);
        number.print();

        Complex added = new Complex(1.0, -13.0);
        number.add(added);
        number.print("after adding", added);

        Complex subtracted = new Complex(11.1, 2.4);
        number.sub(subtracted);
        number.print("after subtracting", subtracted);

        Complex addedAgain = new Complex(-3.3, 1.2);
        number.add(addedAgain);
        number.print("after adding", addedAgain);
    }
}