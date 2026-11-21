public class P2 {
    double salary;
    int merit;
    String grade;

    public void determineGrade() {
        if (salary >= 700) {
            grade = (merit < 20) ? "B" : "A";
        } else if (salary >= 600) {
            grade = (merit < 10) ? "C" : "B";
        } else {
            grade = "C";
        }
    }

    public static void main(String[] args) {
        try (java.util.Scanner sc = new java.util.Scanner(System.in)) {
            P2 person = new P2();

            System.out.print("Enter salary: ");
            person.salary = sc.nextDouble();
            System.out.print("Enter merit points: ");
            person.merit = sc.nextInt();

            person.determineGrade();
            System.out.printf("salary: $%.0f, merit: %d - Grade %s%n", person.salary, person.merit, person.grade);
        }
    }

}
