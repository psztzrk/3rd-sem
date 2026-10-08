public abstract class Character {
    protected String name;
    public String getName() {
        return name;
    }

    protected int healthPoints;
    protected int attackPoints;

    protected Character(String name, int healthPoints, int attackPoints){
        this.name = name;
        this.healthPoints = healthPoints;
        this.attackPoints = attackPoints;
    }

    public void attack(Character target){
        target.handleIncomingAttack(this.attackPower)
    }

}
