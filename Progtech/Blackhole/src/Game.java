public class Game {

    private Board board;
    private CellType currentPlayer;

    private int greyAbsorbed;
    private int blueAbsorbed;

    public Game(int size) {
        board = new Board(size);

        currentPlayer = CellType.BLUE_SHIP;

        greyAbsorbed = 0;
        blueAbsorbed = 0;
    }

    public Board getBoard(){
        return board;
    }

    public CellType getCurrentPlayer() {
        return currentPlayer;
    }

    public MoveResult makeMove(int row, int col, Direction direction){
        // csak a current jtekos hajoja mozoghat
        if (board.getCell(row, col) != currentPlayer) {
            return MoveResult.BLOCKED;
        }

        MoveResult result = board.moveShip(row, col, direction);

        //kor halad tovabb ha mozgott vagy feketelyuk
        if (result == MoveResult.ABSORBED) {

            if (currentPlayer == CellType.GREY_SHIP) {
                greyAbsorbed++;
            } else {
                blueAbsorbed++;
            }
        }

        if (result == MoveResult.MOVED ||
                result == MoveResult.ABSORBED) {
            switchTurn();
        }

        return result;
    }

    private void switchTurn(){
        if (currentPlayer == CellType.BLUE_SHIP) {
            currentPlayer = CellType.GREY_SHIP;
        } else {
            currentPlayer = CellType.BLUE_SHIP;
        }
    }

    public boolean gameOver(){
        int requiredAbs = board.getSize() / 2;

        return greyAbsorbed >= requiredAbs || blueAbsorbed >= requiredAbs;
    }

    public CellType getWinner(){
        int requiredAbs = board.getSize() / 2;

        if (greyAbsorbed >= requiredAbs) {
            return CellType.GREY_SHIP;
        }

        if (blueAbsorbed >= requiredAbs) {
            return CellType.BLUE_SHIP;
        }

        return null;
    }
}
