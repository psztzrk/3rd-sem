package string.utils;

public class IterLetter {
    private String text;
    private int index;

    public IterLetter(String text) {
        if (text == null) {
            throw new IllegalArgumentException("The text must not be null.");
        }
        this.text = text;
        this.reset();
    }

    public void printNext() {
        if (hasNext()) {
            IO.println(text.charAt(index++));
        } else {
            IO.println();
        }
    }

    public void next() {
        index += 1;
    }

    public void reset() {
        index = 0;
    }

    public boolean hasNext() {
        return index < text.length();
    }
}