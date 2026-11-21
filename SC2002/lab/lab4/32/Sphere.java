
public class Sphere implements Shape {
    private Circle circle;

    public Sphere(double radius) {
        this.circle = new Circle(radius);
    }

    public double getArea() {
        return 4 * circle.getArea();
    }
}
