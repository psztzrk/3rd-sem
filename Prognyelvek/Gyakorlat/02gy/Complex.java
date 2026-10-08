public class Complex {
    public double re;
    public double im;

    public Complex(double re, double im)
    {
        this.re = re;
        this.im = im;
    }

    public double abs()
    {
        double d = Math.sqrt(re*re+im);
        return d;
    }

    public void add(Complex c){
        this.re += c.im;
        this.im += c.im;
    }

   // public String getText(){
        
    //}
}

void main(){

}
