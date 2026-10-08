package hallgato;

public class Person {
    private String name;
    private int average;
    private String natinonality;
    
    public Person(String name, int average, String nationality){
        this.name = name;
        this.average = average;
        this.natinonality = nationality;

    }
    public String getName(){
        return this.name;
    }

    public void setName(String name){
        this.name = name;
    }

    public int getAverage(){
        return this.average;
    }

    public void setAverage(int average){
        this.average = average;
    }

    public String getNationality(){
        return this.natinonality;
    }

    public void setNationality(String nationality){
        this.natinonality = nationality;
    }
}
