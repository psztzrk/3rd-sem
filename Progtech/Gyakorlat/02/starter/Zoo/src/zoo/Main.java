package zoo;

import zoo.entities.Animal;
import zoo.entities.Caretaker;
import zoo.entities.Cat;
import zoo.entities.Elephant;

import java.lang.classfile.attribute.CodeAttribute;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        Caretaker caretaker = new Caretaker();
        Cat cat = new Cat();
        Elephant elephant = new Elephant();
        List<Animal> animals = List.of(cat, elephant, new Elephant());

        caretaker.takeCareOf(cat);
        caretaker.takeCareOf(animals);

        animals.getFirst();
    }
}
