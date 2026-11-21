package lab3;

public class PlaneApp {
    public static void main(String[] args) {
        Plane plane = new Plane(); // assuming 12 seats
        java.util.Scanner sc = new java.util.Scanner(System.in);
        int option;

        do {
            System.out.println("\n=== Plane Seating Reservation System ===");
            System.out.println("(1) Show number of empty seats");
            System.out.println("(2) Show list of empty seats");
            System.out.println("(3) Show customers by seat number");
            System.out.println("(4) Show customers by customer ID");
            System.out.println("(5) Assign customer to seat");
            System.out.println("(6) Remove seat assignment");
            System.out.println("(7) Quit");
            System.out.print("Select an option: ");
            option = sc.nextInt();
            sc.nextLine();

            switch (option) {
                case 1:
                    plane.showNumEmptySeats();
                    break;
                case 2:
                    plane.showEmptySeats();
                    break;
                case 3:
                    plane.showAssignedSeats(true);
                    break;
                case 4:
                    plane.showAssignedSeats(false);
                    break;
                case 5:
                    System.out.print("Enter seat number: ");
                    int seatNum = sc.nextInt();
                    System.out.print("Enter customer ID: ");
                    int custId = sc.nextInt();
                    plane.assignSeat(seatNum, custId);
                    break;
                case 6:
                    System.out.print("Enter seat number: ");
                    int seat = sc.nextInt();
                    plane.unAssignSeat(seat);
                    break;
                case 7:
                    System.out.println("Thank you for using the system!");
                    break;
                default:
                    System.out.println("Invalid option. Please try again.");
            }
        } while (option != 7);

        sc.close();
    }

}
