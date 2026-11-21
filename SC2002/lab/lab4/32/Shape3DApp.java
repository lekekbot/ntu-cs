
import java.util.Scanner;

public class Shape3DApp {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the total number of shapes: ");
        int numShapes = scanner.nextInt();
        
        Shape[] shapes = new Shape[numShapes];

        for (int i = 0; i < numShapes; i++) {
            System.out.println("\nShape " + (i + 1));
            System.out.println("Choose the shape:");
            System.out.println("1. Sphere");
            System.out.println("2. Square-based Pyramid");
            System.out.println("3. Cuboid");
            System.out.println("4. Cone");
            System.out.println("5. Cylinder");
            System.out.print("Enter choice: ");
            int choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter radius of Sphere: ");
                    double radius = scanner.nextDouble();
                    shapes[i] = new Sphere(radius);
                    break;
                case 2:
                    System.out.print("Enter base side of Pyramid: ");
                    double baseSide = scanner.nextDouble();
                    System.out.print("Enter slant height of Pyramid: ");
                    double slantHeight = scanner.nextDouble();
                    shapes[i] = new Pyramid(baseSide, slantHeight);
                    break;
                case 3:
                    System.out.print("Enter length of Cuboid: ");
                    double length = scanner.nextDouble();
                    System.out.print("Enter breadth of Cuboid: ");
                    double breadth = scanner.nextDouble();
                    System.out.print("Enter height of Cuboid: ");
                    double height = scanner.nextDouble();
                    shapes[i] = new Cuboid(length, breadth, height);
                    break;
                case 4:
                    System.out.print("Enter radius of Cone: ");
                    double coneRadius = scanner.nextDouble();
                    System.out.print("Enter slant height of Cone: ");
                    double coneSlantHeight = scanner.nextDouble();
                    shapes[i] = new Cone(coneRadius, coneSlantHeight);
                    break;
                case 5:
                    System.out.print("Enter radius of Cylinder: ");
                    double cylRadius = scanner.nextDouble();
                    System.out.print("Enter height of Cylinder: ");
                    double cylHeight = scanner.nextDouble();
                    shapes[i] = new Cylinder(cylRadius, cylHeight);
                    break;
                default:
                    System.out.println("Invalid choice.");
                    i--; // Decrement to retry
                    break;
            }
        }

        System.out.println("\nChoose the type of calculation:");
        System.out.println("1. Calculate Surface Area");
        // Future plan for Volume
        System.out.print("Enter choice: ");
        int calcChoice = scanner.nextInt();

        if (calcChoice == 1) {
            double totalArea = 0;
            for (Shape shape : shapes) {
                totalArea += shape.getArea();
            }
            System.out.println("\nTotal Surface Area of the 3-D figure: " + totalArea);
        } else {
            System.out.println("Calculation not supported yet.");
        }
        
        scanner.close();
    }
}
