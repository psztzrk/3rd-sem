public class Complex {
    double re;
    double im;

    public Complex(double re, double im) {
        this.re = re;
        this.im = im;
    }

    public double abs() {
        return Math.sqrt(re * re + im * im);
    }

    public void add(Complex complex) {
        re += complex.re;
        im += complex.im;
    }

    public void sub(Complex complex) {
        add(new Complex(-complex.re, -complex.im));
    }

    public void mul(Complex complex) {
        double newRe = re * complex.re - im * complex.im;
        double newIm = re * complex.im + im * complex.re;
        re = newRe;
        im = newIm;
    }

    public void conjugate() {
        im = -im;
    }

    public void reciprocate() {
        double denominator = re * re + im * im;
        if (denominator == 0.0) {
            throw new ArithmeticException("Zero has no reciprocal.");
        }
        re /= denominator;
        im = -im / denominator;
    }

    public void div(Complex complex) {
        Complex reciprocal = new Complex(complex.re, complex.im);
        reciprocal.reciprocate();
        mul(reciprocal);
    }

    public String getText() {
        if (im == 0.0) {
            return "%2.1f".formatted(re);
        }
        return "%2.1f%s%2.1fi".formatted(re, im > 0.0 ? "+" : "", im);
    }

    public void print() {
        IO.println("The number is " + getText());
    }

    public void print(String text, Complex complex) {
        IO.println("The number is %s %s %s".formatted(getText(), text, complex.getText()));
    }
}