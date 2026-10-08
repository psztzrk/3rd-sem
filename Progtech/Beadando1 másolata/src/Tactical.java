public class Tactical extends Player{

    private int buyOpportunity;

    public Tactical(String name){
        super(name);
        buyOpportunity = 0;
    }

    @Override
    public void buy(Estate estate) {
        buyOpportunity++;

        if (buyOpportunity % 2 == 0) {
            return;
        }

        if (money >= 1000) {
            pay(1000);

            estate.setOwner(this);
            addProperties(estate);
        }
    }
}


