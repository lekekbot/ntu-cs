import java.util.Scanner;

public class P1 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter your choice (A/C/D): ");
        String choice = sc.nextLine();

        switch (choice.toUpperCase()) {
        case "A":
            System.out.println("Action movie fan\n");
            break;
        case "C ":
            System.out.println("Comedy movie fan\n");
            break;
        case "D":
            System.out.println("Drama movie fan\n");
            break;
        default:
            System.out.println("Invalid choice");
            break;
        }
    }
}
