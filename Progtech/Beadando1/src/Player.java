public abstract class Player {
    protected String name;
    protected int money;
    protected int boardPosition;
    protected Estate[] properties;
    protected int propertyCount;

    public Player(String name){
        this.name = name;
        money = 10000;
        boardPosition = 0;

        properties = new Estate[100];
        propertyCount = 0;

    }

    public String getName(){
        return name;
    }
    public int getMoney(){
        return money;
    }
    public int getBoardPosition(){
        return boardPosition;
    }


    public void move(int rolled, int boardSize){  //kell a boardsize is a leosztás miatt
        boardPosition = (boardPosition + rolled) % boardSize;
        //hozzáad és leosztás után a maradék meg pontosan azt a mezőt adja ahová lép a játékos a boardon
    }

    public void addProperties(Estate estate){
        properties[propertyCount] = estate;
        propertyCount++;
    }

    public Field[] getProperties(){
        return properties;
    }

    public int getPropertyCount(){
        return propertyCount;
    }


    public void pay(int amount){
        money -= amount;
    }

    public void get(int amount){
        money += amount;
    }

    public abstract void buy(Estate estate);

    public void buildAHouse(Estate estate){
        if (!estate.hasHouse && money >= 4000)
        {
            pay(4000);
            estate.buildAHouse();
        }
    }

    public int getHouseCount(){
        int count = 0;
        for (int i = 0; i < propertyCount; i++) {
            if (properties[i].hasHouse)
            {
                count++;
            }
        }
        return count;
    }

    public boolean isBankrupt(){
        return money < 0;
    }
}
