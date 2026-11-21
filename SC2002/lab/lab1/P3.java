public class P3 {
    static double conversion = 1.82;
    static double starting;
    static double ending;
    static int increment;

    public static void main(String[] args) {
        java.util.Scanner sc = new java.util.Scanner(System.in);

        System.out.print("Starting: ");
        starting = sc.nextDouble();
        System.out.print("Ending: ");
        ending = sc.nextDouble();
        System.out.print("Increment: ");
        increment = sc.nextInt();

        if (starting < 0 || ending < 0 || increment <= 0 || starting > ending) {
            System.out.println("Invalid input");
        } else {
            table1();
            table2();
            table3();

        }
        sc.close();

    }

    public static void table1() {
        System.out.printf("%-10s %-10s%n", "US$", "SG$");
        System.out.println("---------------------");
        for (double i = starting; i <= ending; i += increment) {
            double usd = i * conversion;
            System.out.printf("%-10.2f %-10.2f%n", i, usd);
        }
    }

    public static void table2() {
        System.out.printf("%-10s %-10s%n", "US$", "SG$");
        System.out.println("---------------------");
        double tempStarting = starting;
        while (tempStarting <= ending) {
            double usd = tempStarting * conversion;
            System.out.printf("%-10.2f %-10.2f%n", tempStarting, usd);
            tempStarting += increment;
        }
    }

    public static void table3() {
        System.out.printf("%-10s %-10s%n", "US$", "SG$");
        System.out.println("---------------------");
        double tempStarting = starting;

        do {
            double usd = tempStarting * conversion;
            System.out.printf("%-10.2f %-10.2f%n", tempStarting, usd);
            tempStarting += increment;
        } while (tempStarting <= ending);
    }
}
