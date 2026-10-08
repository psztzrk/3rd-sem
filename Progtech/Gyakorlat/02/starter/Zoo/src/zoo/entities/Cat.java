package zoo.entities;

public class Cat extends Pet
{
    @Override
    public void move(){
        System.out.println("cat struts.");
    }

    @Override
    public void makeSound(){
        System.out.println("Meooowww!");
    }
}
