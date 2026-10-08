public class Greedy extends Player {

    public Greedy(String name){
        super(name);
    }

    @Override
    public void buy(Estate estate){
        if (money >= 1000){
            pay(1000);

            estate.setOwner(this);
            addProperties(estate);
        }
    }
}
