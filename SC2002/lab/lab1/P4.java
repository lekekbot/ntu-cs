public class P4 {
    static String a = "AA";
    static String b = "BB";
    static int height;

    public static void main(String[] args) {
        try (java.util.Scanner sc = new java.util.Scanner(System.in)) {
            System.out.print("Height: ");
            height = sc.nextInt();

            if(height == 0) {
                System.out.println("Invalid height");
                return;
            }

            for (int i = 1; i <= height; i++) {
                String temp = "";
                // int tempIdx = 0
                for (int tempIdx = 1; tempIdx <= i; tempIdx++) {
                    if (tempIdx % 2 == 0) {
                        temp = b + temp;
                    } else {
                        temp = a + temp;
                    }e
                }
                System.out.println(temp);
            }
        }
    }

}
