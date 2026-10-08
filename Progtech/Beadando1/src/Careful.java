public class Careful extends Player{
    public Careful(String name){
        super(name);
    }

    @Override
    public void buy(Estate estate) {
        if (money >= 1000 && money - 1000 >= money / 2) {
            pay(1000);

            estate.setOwner(this);
            addProperties(estate);
        }
    }
}
