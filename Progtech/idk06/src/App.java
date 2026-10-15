import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.function.IntBinaryOperator;

public class App {
    private JTextField operand1Field;
    private JTextField operand2Field;
    private JTextField resultField;
    private static int TEXTFIELD_WIDTH = 30;
    public App(){

        JFrame frame = new JFrame("Calc - short for Calculator");
        frame.setVisible(true);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);


        JPanel fieldPanel = new JPanel();

        JTextField operand1Field = new JTextField(TEXTFIELD_WIDTH);
        JTextField operand2Field = new JTextField(TEXTFIELD_WIDTH);
        JTextField resultField = new JTextField(TEXTFIELD_WIDTH);
        resultField.setEditable(false);

        fieldPanel.add(operand1Field);
        fieldPanel.add(operand2Field);
        fieldPanel.add(resultField);

        JPanel buttonPanel = new JPanel();
        JButton additionButton = new JButton(" + ");
        fieldPanel.add(additionButton);
        additionButton.addActionListener(new CalcActionListener(Math::addExact));
        JButton subtractionButton = new JButton(" - ");
        fieldPanel.add(subtractionButton);
        additionButton.addActionListener(new CalcActionListener(Math::subtractExact));
        JButton multiplicationButton = new JButton(" * ");
        fieldPanel.add(multiplicationButton);
        additionButton.addActionListener(new CalcActionListener(Math::multiplyExact));
        JButton divisionButton = new JButton(" / ");
        fieldPanel.add(divisionButton);
        additionButton.addActionListener(new CalcActionListener(Math::divideExact));
        JButton powerButton = new JButton(" ^ ");
        fieldPanel.add(powerButton);
        additionButton.addActionListener(new CalcActionListener((op1, op2) -> Math.toIntExact(Math.round(Math.pow(op1,op2)))));


        frame.add(fieldPanel, BorderLayout.NORTH);
        frame.add(buttonPanel, BorderLayout.EAST);

    }

    class CalcActionListener implements ActionListener {
        private final IntBinaryOperator op;

        public CalcActionListener(IntBinaryOperator op){
            this.op = op;
        }

        @Override
        public void actionPerformed(ActionEvent e){
            try {
                Integer op1 = Integer.parseInt(operand1Field.getText());
                Integer op2 = Integer.parseInt(operand2Field.getText());
                Integer result = op.applyAsInt(op1, op2);


            }catch (Exception ex){

            }
        }
    }
}
