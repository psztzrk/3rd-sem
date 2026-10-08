package string.utils.main;

import string.utils.IterLetter;

public class Main {
    public static void main(String... args) {
        if (args.length < 2 || args.length > 4) {
            throw new IllegalArgumentException("Use: count text [beforeReset afterReset]");
        }

        IterLetter iterator = new IterLetter(args[1]);

        if (args.length == 2) {
            print(iterator, Integer.parseInt(args[0]));
            return;
        }

        int beforeReset = Integer.parseInt(args[2]);
        int afterReset = Integer.parseInt(args[3]);
        print(iterator, beforeReset);
        IO.println(iterator.hasNext());
        iterator.reset();
        IO.println(iterator.hasNext());
        print(iterator, afterReset);
        IO.println(iterator.hasNext());
    }

    private static void print(IterLetter iterator, int count) {
        for (int idx = 0; idx < count; idx++) {
            iterator.printNext();
        }
    }
}