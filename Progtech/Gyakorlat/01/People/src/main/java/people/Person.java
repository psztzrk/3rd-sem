package people;

public class Person {
    private String name;
    private int age;
    private String natinonality;
    
    public Person(String name, int age, String nationality){
        this.name = name;
        this.age = age;
        this.natinonality = nationality;

    }
    public String getName(){
        return this.name;
    }

    public void setName(String name){
        this.name = name;
    }

    public int getAge(){
        return this.age;
    }

    public void setAge(int age){
        this.age = age;
    }

    public String getNationality(){
        return this.natinonality;
    }

    public void setNationality(String nationality){
        this.natinonality = nationality;
    }

}