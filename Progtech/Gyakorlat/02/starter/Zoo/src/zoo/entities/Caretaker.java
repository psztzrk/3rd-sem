package zoo.entities;

import java.util.List;

public class Caretaker {
    public void takeCareOf(Animal animal){
        System.out.println("Caretaker took care of" + " " + animal.getClass().getSimpleName());
    }

    public void takeCareOf(List<Animal> animals){
        animals.forEach(this::takeCareOf);  //for ciklus basically, : -> metódus referencia


    }

}
