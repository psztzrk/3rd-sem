import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;


public class FileReader {

    public static Game read(String fileName) throws FileNotFoundException{
        Scanner scanner = new Scanner(new File(fileName));
        // üres file
        if (!scanner.hasNext()) {
            scanner.close();
            throw new IllegalArgumentException();
        }


        // pálya
        int fieldCount = scanner.nextInt();

        ArrayList<Field> fields = new ArrayList<>();

        for (int i = 0; i < fieldCount; i++){
            String type = scanner.next();

            if (type.equals("E"))
            {
                fields.add(new Estate());
            }
            else if (type.equals("S"))
            {
                int amount = scanner.nextInt();
                fields.add(new Service(amount));
            }
            else if (type.equals("L"))
            {
                int amount = scanner.nextInt();
                fields.add(new Luck(amount));
            }
        }

        Board board = new Board(fields);

        // játékosok
        int playersCount = scanner.nextInt();

        ArrayList<Player> players = new ArrayList<>();

        for (int i = 0; i < playersCount; i++)
        {
             String name = scanner.next();

             String tactic = scanner.next();

             if (tactic.equals("greedy"))
             {
                 players.add(new Greedy(name));
             }
             else if (tactic.equals("careful"))
             {
                 players.add(new Careful(name));
             }
             if (tactic.equals("tactical"))
             {
                 players.add(new Tactical(name));
             }
        }

        // dobások
        ArrayList<int[]> rolls = new ArrayList<>();
        //körönként beolvassa és eltárolja -> 1 kör, 1 tömb
        while(scanner.hasNextInt()){
            int[] round = new int[playersCount];

            for (int i = 0; i < playersCount; i++) {
                round[i] = scanner.nextInt();
            }

            rolls.add(round);
        }
        scanner.close();

        int[][] rollArray = new int[rolls.size()][];

        for (int i = 0; i < rolls.size(); i++)
        {
             rollArray[i] = rolls.get(i);
        }

        Game game = new Game(board, players, rollArray);

        return game;
    }

}
