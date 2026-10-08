public class Estate extends Field{
    private Player owner;
    public boolean hasHouse;
    final int price;

    public Estate(){
        owner = null;
        hasHouse = false;
        price = 1000;
    }

    public  Player getOwner(){
        return owner;
    }

    public  void setOwner(Player owner){
        this.owner =  owner;
    }

    public boolean getHouse(){
        return hasHouse;
    }

    public int getPrice(){
        return price;
    }

    public void buildAHouse(){
        hasHouse = true;
    }

    public void removeHouse(){
        hasHouse = false;
    }

    @Override
    public void playOut(Player player){
        // még senkié
        if (owner == null){
            player.buy(this);
        }
        // a sajátja
        else if(owner == player && !hasHouse){
            player.buildAHouse(this);
        }
        // másé
        else {
            if (hasHouse){
                player.pay(2000);
                owner.get(2000);
            }
            else {
                player.pay(500);
                owner.get(500);
            }
        }

    }
}
