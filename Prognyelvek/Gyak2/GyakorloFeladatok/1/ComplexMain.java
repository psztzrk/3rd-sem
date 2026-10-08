import java.util.Locale;

public class ComplexMain {
    public static void main(String... args) {
        Locale.setDefault(Locale.of("hu"));

        Complex number = new Complex(4.0, 2.0);
        number.conjugate();
        number.print();

        number.reciprocate();
        number.print();

        Complex divisor = new Complex(1.0, -1.0);
        number.div(divisor);
        number.print("after dividing by", divisor);
    }
}