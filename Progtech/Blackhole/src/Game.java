public class Game {

    private Board board;


    public Game(int size) {
        board = new Board(size);
    }

    public Board getBoard(){
        return board;
    }

}
