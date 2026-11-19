import model.ColorClickerModel;
import view.ColorClickerGUI;

import javax.swing.*;

public class Main {
    public static void main(String[] args) {
            ColorClickerModel model = new ColorClickerModel();
            model.initializeBoard(10);
            // TODO: create the repository for jdbc:sqlite:colorclicker.db
            // TODO: if that fails (SQLException), show an error dialog and exit
            // TODO: pass the repository to the GUI
            SwingUtilities.invokeLater(() -> new ColorClickerGUI(model));
    }
}