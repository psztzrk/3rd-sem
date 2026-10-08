package zoo.entities;

public class Elephant extends WildAnimal{
    @Override
    public void move() {
        System.out.println("Elephant tramples");
    }

    @Override
    public void makeSound() {
        System.out.println("TRÖÖÖT");
    }
}
