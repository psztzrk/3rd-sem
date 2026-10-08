package queue;

import java.util.ArrayList;
import java.util.List;

public class Queue {
    private List<Integer> data;
    public Queue(){
        this.data = new ArrayList<Integer>();
    }

    public void Push(int elem){
        this.data.add(elem);
    }

    public Integer Pop(){
        return this.data.removeLast();
    }

    public int size(){
        return data.size();
    }
}
