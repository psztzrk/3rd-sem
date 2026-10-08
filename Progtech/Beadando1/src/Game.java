import javax.swing.plaf.IconUIResource;
import java.util.ArrayList;

public class Game {
    private Board board;
    private ArrayList<Player> players;
    private int[][] rolls;

    public Game(Board board, ArrayList<Player> players, int[][] rolls){
        this.board = board;
        this.players = players;
        this.rolls = rolls;
    }

    public void startGame(){
        for (int round = 0; round < rolls.length; round++){

            startRound(rolls[round]);
        }
    }

    private void startRound(int[] roundRolls){
        for (int i = 0; i < players.size(); i++){
            Player player = players.get(i);

            if (player.isBankrupt()){
                eliminate(player);
                continue;
            }

            int rolled = roundRolls[i];

            player.move(rolled, board.getNumberOfFields());

            Field field = board.getField(player.getBoardPosition());

            field.playOut(player);

        }
    }

    private void eliminate(Player player){
        for (Field field : board.getFields()){

            if (field instanceof Estate){
                Estate estate = (Estate) field;

                if (estate.getOwner() == player){
                    estate.setOwner(null);
                    estate.removeHouse();
                }

            }
        }
    }

    public void printResult(){
        System.out.println("------- Players at the certain round -------");

        for (Player player : players){
            System.out.println(player.getName() + " has " + player.getMoney() + " Petak");
            System.out.println("Properties: " + player.propertyCount);
            System.out.println("Houses: " + player.getHouseCount());

            System.out.println();
            System.out.println("---------------------------------------");
        }
    }

}
