import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class Alignment {

    private static double sigmoid(double in) {
        return 1.0d / (1.0d + Math.exp(-in));
    }

    public static void main(String[] args) {
        try{

            BufferedReader featBr = new BufferedReader(new FileReader("tests/data/feature.csv"));
            BufferedReader ansBr = new BufferedReader(new FileReader("tests/data/lgb_predict.csv"));
            String line;
            String answer_s;
            double arr[] = new double[11];
            __LGBC_LGBModel model = new __LGBC_LGBModel();


            while ((line = featBr.readLine()) != null) {
                answer_s = ansBr.readLine();
                double answer = Double.parseDouble(answer_s);

                String[] values = line.split(",");
                for (int i = 0; i < values.length; i++){
                    if (values[i].equals("nan")){
                        arr[i] = model.NaN;
                    } else {
                        arr[i] = Double.parseDouble(values[i]);
                    }
                    System.out.println(arr[i]);
                }
                double predict = sigmoid(model.__LGBC_predict_tree_all(arr));
                System.out.format("%f vs %f %n", answer, predict);
                if (Math.abs(answer - predict) > 1e-6) {
                    System.out.println("alignment test failed");
                    System.exit(1);
                }
            }
            System.out.println("alignment test succeed");

        } catch (IOException e)  {
            e.printStackTrace();
        }
    }
}
