import java.util.ArrayList;
import java.util.Enumeration;

public class Board {
    private ArrayList<Field> fields;

    public  Board(ArrayList<Field> fields){
        this.fields = fields;
    }

    public Field getField(int index){
        return fields.get(index);
    }
    public ArrayList<Field> getFields(){
        return fields;
    }

    public int getNumberOfFields(){
        return  fields.size();
    }

}
