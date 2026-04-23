/** based on code segments from
 * http://download.oracle.com/javase/6/docs/api/java/io/ObjectOutputStream.html
 * and http://download.oracle.com/javase/6/docs/api/java/io/ObjectInputStream.html.
 */
import java.io.*;
import java.util.Date;

public class ObjectInputOutputDemo {

    public static void main(String[] args) {
        try {
            FileOutputStream fos = new FileOutputStream("t.tmp");
            ObjectOutputStream oos = new ObjectOutputStream(fos);

            int od = 12345;
            System.out.print("saving data to t.tmp ...");
            oos.writeInt(od);
            String s = "Today";
            oos.writeObject(s); // write a String object to file
            Date dt = new Date();
            oos.writeObject(dt);  // write a Date object to file
            System.out.printf("Output data: %d\t%s\t%s\n", od, s, dt.toString());
            oos.close();
        } catch (IOException e) {
            System.out.println("File input error");
        }

        try {
            FileInputStream fis = new FileInputStream("t.tmp");
            ObjectInputStream ois = new ObjectInputStream(fis);

            System.out.print("reading data from t.tmp ...");
            int i = ois.readInt();
            String today = (String) ois.readObject();  // read the String object from file
            Date date = (Date) ois.readObject();  // read the Date object from file
            System.out.printf("Input data: %d\t%s\t%s\n", i, today, date.toString());
            ois.close();
        } catch (IOException e) {
            System.out.println("File input error");
        } catch (ClassNotFoundException e) {
            System.out.println(e);
        }
    } // main
} //class

