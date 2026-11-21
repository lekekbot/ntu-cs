
import java.util.Scanner;

public class Shape2DApp {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the total number of shapes: ");
        int numShapes = scanner.nextInt();
        
        Shape[] shapes = new Shape[numShapes];

        for (int i = 0; i < numShapes; i++) {
            System.out.println("\nShape " + (i + 1));
            System.out.println("Choose the shape:");
            System.out.println("1. Square");
            System.out.println("2. Rectangle");
            System.out.println("3. Circle");
            System.out.println("4. Triangle");
            System.out.print("Enter choice: ");
            int choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter side of Square: ");
                    double side = scanner.nextDouble();
                    shapes[i] = new Square(side);
                    break;
                case 2:
                    System.out.print("Enter length of Rectangle: ");
                    double length = scanner.nextDouble();
                    System.out.print("Enter breadth of Rectangle: ");
                    double breadth = scanner.nextDouble();
                    shapes[i] = new Rectangle(length, breadth);
                    break;
                case 3:
                    System.out.print("Enter radius of Circle: ");
                    double radius = scanner.nextDouble();
                    shapes[i] = new Circle(radius);
                    break;
                case 4:
                    System.out.print("Enter base of Triangle: ");
                    double base = scanner.nextDouble();
                    System.out.print("Enter height of Triangle: ");
                    double height = scanner.nextDouble();
                    shapes[i] = new Triangle(base, height);
                    break;
                default:
                    System.out.println("Invalid choice.");
                    i--; // Decrement to retry this iteration
                    break;
            }
        }

        System.out.println("\nChoose the type of calculation:");
        System.out.println("1. Calculate Area");
        // Future plan for Volume
        System.out.print("Enter choice: ");
        int calcChoice = scanner.nextInt();

        if (calcChoice == 1) {
            double totalArea = 0;
            for (Shape shape : shapes) {
                totalArea += shape.getArea();
            }
            System.out.println("\nTotal Area of the 2-D figure: " + totalArea);
        } else {
            System.out.println("Calculation not supported yet.");
        }
        
        scanner.close();
    }
}
