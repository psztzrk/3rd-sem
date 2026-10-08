import java.io.FileNotFoundException;
import java.util.Scanner;

public class Main {

    public static void main(){
        Scanner scanner = new Scanner(System.in);

        try
        {
            System.out.print("What's the name of your file?: ");
            String file = scanner.next();

            Game game = FileReader.read(file);

            game.startGame();

            game.printResult();
        }
        catch (FileNotFoundException e)
        {
            System.out.println("File not found!");
        }
        catch (IllegalArgumentException e){
            System.out.println("That is an empty file mi amigo");
        }
    }

}
