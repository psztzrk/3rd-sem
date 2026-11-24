package model;

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

    public CellType getCell(int row, int col) {
        return cells[row][col];
    }

    public MoveResult moveShip(int row, int col, Direction direction){
        CellType ship = cells[row][col];

        if (ship != CellType.BLUE_SHIP && ship != CellType.GREY_SHIP)
        {
            return MoveResult.BLOCKED;
        }

        int currentRow = row;
        int currentCol = col;

        while(true){
            int nextRow = currentRow;
            int nextCol = currentCol;

            switch (direction){
                case UP:
                    nextRow--;
                    break;

                case DOWN:
                    nextRow++;
                    break;

                case LEFT:
                    nextCol--;
                    break;

                case RIGHT:
                    nextCol++;
                    break;
            }

            // ne lepjen ki a tablarol
            if(nextRow < 0 || nextRow >= size || nextCol < 0 || nextCol >= size){
                break;
            }

            CellType nextCell = cells[nextRow][nextCol];

            // ha feketelyuk
            if(nextCell == CellType.BLACK_HOLE){
                cells[currentRow][currentCol] = CellType.EMPTY;
                return MoveResult.ABSORBED;
            }

            // ha hajoba megy
            if(nextCell != CellType.EMPTY){
                break;
            }

            //mozgas
            cells[nextRow][nextCol] = ship;
            cells[currentRow][currentCol] = CellType.EMPTY;

            currentRow = nextRow;
            currentCol = nextCol;
        }

        if (currentRow == row && currentCol == col){
            return MoveResult.BLOCKED;
        }

        return MoveResult.MOVED;
    }

}
