public class Service extends Field{
    final int amount;
    public Service(int amount){
        this.amount = amount;
    }

    public int getAmount(){
        return amount;
    }

    @Override
    public void playOut(Player player){
        player.pay(amount);
    }
}
