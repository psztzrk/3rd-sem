public class Board {
    private int size;
    private int center;
    private CellType[][] cells;

    public Board(int size){
        this.size = size;
        this.center = size / 2;
        cells = new CellType[size][size];

        initializeBoard();
    }

    private void placeShips(){

        //grey ships
        for (int col = 0; col < center; col++) {
            cells[0][col] = CellType.GREY_SHIP;
        }
        for (int col = center + 1; col < size; col++) {
            cells[0][col] = CellType.GREY_SHIP;
        }

        //blue ships
        for (int col = 0; col < center; col++) {
            cells[size -1][col] = CellType.BLUE_SHIP;
        }
        for (int col = center + 1; col < size; col++) {
            cells[size -1][col] = CellType.BLUE_SHIP;
        }
    }

    private void initializeBoard(){
        // ures indulasi mezok
        for (int row = 0; row < size; row++) {
            for (int col = 0; col < size; col++) {
                cells[row][col] = CellType.EMPTY;
            }
        }

        //blackhole kozepen
        cells[center][center] = CellType.BLACK_HOLE;

        //urhajok
        placeShips();
    }

    public int getSize(){
        return size;
    }

    public CellType getCells(int row, int col) {
        return cells[row][col];
    }
}
