public class Luck extends Field{
    final int amount;
    public Luck(int amount){
        this.amount = amount;
    }

    public int getAmount(){
        return amount;
    }

    @Override
    public void playOut(Player player){
        player.get(amount);
    }
}
